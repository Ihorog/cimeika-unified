package com.cimeika.webview

import android.app.*
import android.content.Context
import android.content.Intent
import android.graphics.*
import android.os.Build
import android.os.IBinder
import android.view.*
import android.widget.ImageView
import androidx.core.app.NotificationCompat

class OverlayService : Service() {

    private var windowManager: WindowManager? = null
    private var overlayView: View? = null
    private var initialX = 0
    private var initialY = 0
    private var initialTouchX = 0f
    private var initialTouchY = 0f
    private var isMoving = false
    private var longPressHandler = android.os.Handler()
    private var downTime = 0L

    companion object {
        private const val NOTIFICATION_ID = 1001
        private const val CHANNEL_ID = "overlay_service_channel"
        private const val LONG_PRESS_DURATION = 500L
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(NOTIFICATION_ID, createNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (overlayView == null) {
            createOverlayView()
        }
        return START_STICKY
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Cimeika Overlay",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Keeps Cimeika overlay button active"
            }
            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Cimeika")
            .setContentText("Overlay active")
            .setSmallIcon(android.R.drawable.ic_menu_compass)
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    private fun createOverlayView() {
        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else
                WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 100
            y = 100
        }

        overlayView = ImageView(this).apply {
            // Create circular icon with gradient
            val size = 56 * resources.displayMetrics.density.toInt()
            layoutParams = ViewGroup.LayoutParams(size, size)
            setImageBitmap(createCiLogo(size))
            scaleType = ImageView.ScaleType.FIT_CENTER
        }

        overlayView?.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = params.x
                        initialY = params.y
                        initialTouchX = event.rawX
                        initialTouchY = event.rawY
                        isMoving = false
                        downTime = System.currentTimeMillis()
                        
                        // Schedule long press check
                        longPressHandler.postDelayed({
                            if (!isMoving) {
                                // Long press detected - enable move mode
                                isMoving = true
                                v.alpha = 0.7f
                            }
                        }, LONG_PRESS_DURATION)
                        return true
                    }
                    MotionEvent.ACTION_MOVE -> {
                        val deltaX = event.rawX - initialTouchX
                        val deltaY = event.rawY - initialTouchY
                        
                        // If moved significantly, consider it a move
                        if (Math.abs(deltaX) > 10 || Math.abs(deltaY) > 10) {
                            isMoving = true
                            longPressHandler.removeCallbacksAndMessages(null)
                        }
                        
                        if (isMoving) {
                            params.x = initialX + deltaX.toInt()
                            params.y = initialY + deltaY.toInt()
                            windowManager?.updateViewLayout(overlayView, params)
                        }
                        return true
                    }
                    MotionEvent.ACTION_UP -> {
                        longPressHandler.removeCallbacksAndMessages(null)
                        v.alpha = 1f
                        
                        val upTime = System.currentTimeMillis()
                        val pressDuration = upTime - downTime
                        
                        // Check if it's a swipe down/away to dismiss
                        val deltaY = event.rawY - initialTouchY
                        val deltaX = event.rawX - initialTouchX
                        
                        if (Math.abs(deltaY) > 200 || Math.abs(deltaX) > 200) {
                            // Swipe detected - dismiss overlay
                            stopSelf()
                            return true
                        }
                        
                        // If not moved much and quick tap, open app
                        if (!isMoving && pressDuration < LONG_PRESS_DURATION) {
                            openApp()
                        }
                        
                        isMoving = false
                        return true
                    }
                }
                return false
            }
        })

        windowManager?.addView(overlayView, params)
    }

    private fun createCiLogo(size: Int): Bitmap {
        val bitmap = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bitmap)
        
        // Draw circular gradient background
        val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            shader = RadialGradient(
                size / 2f, size / 2f, size / 2f,
                intArrayOf(Color.parseColor("#667eea"), Color.parseColor("#764ba2")),
                null,
                Shader.TileMode.CLAMP
            )
        }
        canvas.drawCircle(size / 2f, size / 2f, size / 2f, paint)
        
        // Draw "Ci" text in center
        val textPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.WHITE
            textSize = size * 0.4f
            textAlign = Paint.Align.CENTER
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
        }
        
        val textBounds = Rect()
        textPaint.getTextBounds("Ci", 0, 2, textBounds)
        val textY = size / 2f - textBounds.exactCenterY()
        
        canvas.drawText("Ci", size / 2f, textY, textPaint)
        
        return bitmap
    }

    private fun openApp() {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
        }
        startActivity(intent)
    }

    override fun onDestroy() {
        overlayView?.let {
            windowManager?.removeView(it)
        }
        longPressHandler.removeCallbacksAndMessages(null)
        super.onDestroy()
    }
}
