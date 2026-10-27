// Appli Sensor Maps : l'interface (HTML) dans une WebView, fabriquée par GitHub Actions.
plugins {
    id("com.android.application") version "9.4.1"
}

// Sur GitHub, le numéro du passage sert de numéro de version : chaque nouvel APK s'installe par-dessus l'ancien.
val numero = (System.getenv("NUMERO_VERSION") ?: "1").toInt()

android {
    namespace = "io.github.loscripts.sensormaps"
    compileSdk = 37

    defaultConfig {
        applicationId = "io.github.loscripts.sensormaps"
        minSdk = 26
        targetSdk = 36
        versionCode = numero
        versionName = "maquette-$numero"
    }

    // Clé de test publique : elle ne protège rien, elle permet seulement d'installer
    // chaque nouvelle version par-dessus l'ancienne. Pour Google Play, il faudra une vraie clé, secrète.
    signingConfigs {
        create("test") {
            storeFile = file("cle-de-test-publique.jks")
            storePassword = "sensormaps"
            keyAlias = "test"
            keyPassword = "sensormaps"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("test")
        }
    }

    buildFeatures {
        buildConfig = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    lint {
        checkReleaseBuilds = false
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.19.1")
    implementation("androidx.activity:activity-ktx:1.10.1")
    implementation("androidx.webkit:webkit:1.12.1")
    implementation("androidx.core:core-splashscreen:1.0.1")
}
