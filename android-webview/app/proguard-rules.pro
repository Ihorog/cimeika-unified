# Add project specific ProGuard rules here.
# Keep JavaScript interfaces
-keepattributes JavascriptInterface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep Android WebView
-keep class android.webkit.** { *; }
