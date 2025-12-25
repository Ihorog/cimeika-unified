package com.cimeika.webview

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.speech.RecognizerIntent
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.result.contract.ActivityResultContracts

class MainActivity : Activity() {

    private lateinit var webView: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)
        setContentView(webView)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.webViewClient = WebViewClient()

        webView.addJavascriptInterface(VoiceBridge(), "Android")

        // 🔗 ЖИВИЙ ІНТЕРФЕЙС З VERCEL
        webView.loadUrl("https://cimeika-unified.vercel.app")
    }

    inner class VoiceBridge {
        @JavascriptInterface
        fun startVoice() {
            val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "uk-UA")
            speechLauncher.launch(intent)
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

    private fun json(s: String) = "\"" + s.replace("\"", "\\\"") + "\""
}
