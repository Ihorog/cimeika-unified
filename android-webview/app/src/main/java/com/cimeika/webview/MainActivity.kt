package com.cimeika.webview

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.speech.RecognizerIntent
import android.speech.tts.TextToSpeech
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.util.*

class MainActivity : Activity(), TextToSpeech.OnInitListener {

    private lateinit var webView: WebView
    private var textToSpeech: TextToSpeech? = null
    private var ttsReady = false

    companion object {
        private const val REQUEST_RECORD_AUDIO = 1
        private const val REQUEST_OVERLAY = 2
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)
        setContentView(webView)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.webViewClient = WebViewClient()

        webView.addJavascriptInterface(VoiceBridge(), "Android")

        // Initialize TextToSpeech
        textToSpeech = TextToSpeech(this, this)

        // Check and request RECORD_AUDIO permission
        checkAudioPermission()

        // 🔗 ЖИВИЙ ІНТЕРФЕЙС З VERCEL
        webView.loadUrl("https://cimeika-unified.vercel.app")
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            // Set Ukrainian as default language
            val result = textToSpeech?.setLanguage(Locale("uk", "UA"))
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                // Fallback to English if Ukrainian not available
                textToSpeech?.setLanguage(Locale.US)
            }
            ttsReady = true
        } else {
            Toast.makeText(this, "TTS initialization failed", Toast.LENGTH_SHORT).show()
        }
    }

    private fun checkAudioPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECORD_AUDIO),
                REQUEST_RECORD_AUDIO
            )
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        when (requestCode) {
            REQUEST_RECORD_AUDIO -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(this, "Voice permission granted", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this, "Voice permission denied", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    inner class VoiceBridge {
        @JavascriptInterface
        fun startVoice() {
            // Check permission before starting
            if (ContextCompat.checkSelfPermission(this@MainActivity, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
                runOnUiThread {
                    Toast.makeText(this@MainActivity, "Please grant audio permission", Toast.LENGTH_SHORT).show()
                }
                return
            }

            val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "uk-UA")
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Говоріть зараз...")
            speechLauncher.launch(intent)
        }

        @JavascriptInterface
        fun speak(text: String) {
            if (!ttsReady) {
                runOnUiThread {
                    Toast.makeText(this@MainActivity, "TTS not ready", Toast.LENGTH_SHORT).show()
                }
                return
            }

            runOnUiThread {
                textToSpeech?.speak(text, TextToSpeech.QUEUE_FLUSH, null, null)
            }
        }

        @JavascriptInterface
        fun enableOverlay() {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if (!Settings.canDrawOverlays(this@MainActivity)) {
                    val intent = Intent(
                        Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse("package:${this@MainActivity.packageName}")
                    )
                    overlayPermissionLauncher.launch(intent)
                } else {
                    startOverlayService()
                }
            } else {
                startOverlayService()
            }
        }

        @JavascriptInterface
        fun disableOverlay() {
            runOnUiThread {
                val intent = Intent(this@MainActivity, OverlayService::class.java)
                stopService(intent)
            }
        }
    }

    private fun startOverlayService() {
        runOnUiThread {
            val intent = Intent(this, OverlayService::class.java)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                startForegroundService(intent)
            } else {
                startService(intent)
            }
            Toast.makeText(this, "Overlay enabled", Toast.LENGTH_SHORT).show()
        }
    }

    private val speechLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == RESULT_OK) {
                val data = result.data
                val text =
                    data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
                        ?.firstOrNull() ?: ""

                // 🔁 ПОВЕРТАЄМО ТЕКСТ У WEB
                webView.post {
                    webView.evaluateJavascript(
                        "window.onVoiceText && window.onVoiceText(${json(text)})",
                        null
                    )
                }
            }
        }

    private val overlayPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { _ ->
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                if (Settings.canDrawOverlays(this)) {
                    startOverlayService()
                } else {
                    Toast.makeText(this, "Overlay permission denied", Toast.LENGTH_SHORT).show()
                }
            }
        }

    private fun json(s: String) = "\"" + s.replace("\"", "\\\"") + "\""

    override fun onDestroy() {
        textToSpeech?.stop()
        textToSpeech?.shutdown()
        super.onDestroy()
    }

    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
