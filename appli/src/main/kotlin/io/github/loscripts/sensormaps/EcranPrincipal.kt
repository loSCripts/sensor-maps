package io.github.loscripts.sensormaps

import android.annotation.SuppressLint
import android.content.ActivityNotFoundException
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.View
import android.webkit.ConsoleMessage
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.enableEdgeToEdge
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.core.view.ViewCompat
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.webkit.WebViewAssetLoader

/** L'écran unique : l'interface de Sensor Maps (fichiers HTML de l'appli) dans une WebView. */
class EcranPrincipal : ComponentActivity() {
    private lateinit var vue: WebView
    private var pageChargee = false
    private var margeHaut = 0f
    private var margeBas = 0f
    private var margeGauche = 0f
    private var margeDroite = 0f

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(etatSauve: Bundle?) {
        installSplashScreen()
        super.onCreate(etatSauve)
        // Android 15 et plus dessinent l'appli sous les barres du système : la page reçoit leur taille
        enableEdgeToEdge()

        // Les fichiers de l'interface sont servis depuis l'appli elle-même, sans internet
        val chargeur = WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(this))
            .build()

        vue = WebView(this).apply {
            setBackgroundColor(if (systemeSombre()) Color.BLACK else Color.WHITE)
            overScrollMode = View.OVER_SCROLL_NEVER
            isVerticalScrollBarEnabled = false
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.setSupportZoom(false)
            settings.builtInZoomControls = false
            settings.displayZoomControls = false
            settings.allowFileAccess = false
            settings.allowContentAccess = false
            webViewClient = object : WebViewClient() {
                override fun shouldInterceptRequest(view: WebView, demande: WebResourceRequest): WebResourceResponse? =
                    chargeur.shouldInterceptRequest(demande.url)

                // Les liens vers internet (la carte en ligne, les sources) s'ouvrent dans le navigateur
                override fun shouldOverrideUrlLoading(view: WebView, demande: WebResourceRequest): Boolean {
                    if (demande.url.host == HOTE) return false
                    ouvrirDehors(demande.url)
                    return true
                }

                override fun onPageFinished(view: WebView, adresse: String) {
                    pageChargee = true
                    envoyerMarges()
                }
            }
            webChromeClient = object : WebChromeClient() {
                override fun onConsoleMessage(message: ConsoleMessage): Boolean {
                    Log.i(TAG, message.message())
                    return true
                }
            }
            addJavascriptInterface(Pont(), "SensorMaps")
        }
        setContentView(vue)

        ViewCompat.setOnApplyWindowInsetsListener(vue) { _, insets ->
            val b = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout())
            val d = resources.displayMetrics.density
            margeHaut = b.top / d
            margeBas = b.bottom / d
            margeGauche = b.left / d
            margeDroite = b.right / d
            envoyerMarges()
            WindowInsetsCompat.CONSUMED
        }

        // Le geste retour revient à l'écran d'avant ; depuis l'accueil, il ferme l'appli
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                vue.evaluateJavascript("window.sensorMapsRetour ? window.sensorMapsRetour() : false") { r ->
                    if (r != "true") finish()
                }
            }
        })

        // Après un passage clair ou sombre, la page repart de zéro : ce qui compte est gardé dans la page
        vue.loadUrl("https://$HOTE/assets/index.html")
    }

    override fun onDestroy() {
        vue.destroy()
        super.onDestroy()
    }

    private fun systemeSombre(): Boolean =
        (resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES

    private fun envoyerMarges() {
        if (!pageChargee) return
        vue.evaluateJavascript(
            "window.sensorMapsMarges && window.sensorMapsMarges($margeHaut, $margeBas, $margeGauche, $margeDroite)", null
        )
    }

    /** Icônes des barres du système en noir sur fond clair, en blanc sur fond sombre. */
    private fun appliquerTheme(sombre: Boolean) {
        val barres = WindowCompat.getInsetsController(window, window.decorView)
        barres.isAppearanceLightStatusBars = !sombre
        barres.isAppearanceLightNavigationBars = !sombre
        val fond = if (sombre) Color.BLACK else Color.WHITE
        window.decorView.setBackgroundColor(fond)
        vue.setBackgroundColor(fond)
    }

    private fun ouvrirDehors(adresse: Uri) {
        try {
            startActivity(Intent(Intent.ACTION_VIEW, adresse))
        } catch (e: ActivityNotFoundException) {
            Log.w(TAG, "Aucune appli pour ouvrir $adresse")
        }
    }

    /** Ce que la page peut demander à l'appli. */
    inner class Pont {
        @JavascriptInterface
        fun theme(sombre: Boolean) {
            runOnUiThread { appliquerTheme(sombre) }
        }

        @JavascriptInterface
        fun version(): String = BuildConfig.VERSION_NAME
    }

    private companion object {
        const val TAG = "SensorMaps"
        const val HOTE = "appassets.androidplatform.net"
    }
}
