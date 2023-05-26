package com.unico.check_sdk_poc

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.TextView
import com.acesso.acessobio_android.AcessoBioListener
import com.acesso.acessobio_android.iAcessoBioDocument
import com.acesso.acessobio_android.iAcessoBioSelfie
import com.acesso.acessobio_android.onboarding.AcessoBio
import com.acesso.acessobio_android.onboarding.camera.CameraListener
import com.acesso.acessobio_android.onboarding.camera.UnicoCheckCameraOpener
import com.acesso.acessobio_android.onboarding.camera.document.DocumentCameraListener
import com.acesso.acessobio_android.onboarding.types.DocumentType
import com.acesso.acessobio_android.services.dto.ErrorBio
import com.acesso.acessobio_android.services.dto.ResultCamera

var TAG = "MainActivity"

class MainActivity : AppCompatActivity(), AcessoBioListener,
    iAcessoBioSelfie, CameraListener,
    iAcessoBioDocument, DocumentCameraListener {

    lateinit var textField: TextView
    lateinit var documentType: DocumentType
    val unicoTheme = UnicoTheme()
    val timeout = 50.0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        textField = findViewById(R.id.mainText)
    }

    fun openCameraManual(view : View){
        AcessoBio(this, this)
            .setAutoCapture(false)
            .setSmartFrame(false)
            .setTheme(this.unicoTheme)
            .setTimeoutSession(this.timeout)
            .build()
            .prepareCamera(UnicoConfig(), this@MainActivity)
    }

    fun openCameraSmart(view: View){
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .setTheme(this.unicoTheme)
            .setTimeoutSession(this.timeout)
            .build()
            .prepareCamera(UnicoConfig(), this@MainActivity)
    }

    fun openCameraLiveness(view: View){
        Log.d(TAG, "openCameraLiveness")
        try {
            AcessoBio(this, this)
                .setTheme(this.unicoTheme)
                .setTimeoutSession(this.timeout)
                .build()
                .prepareCamera(UnicoConfigLiveness(), this@MainActivity)
        } catch(e: Exception) {
            Log.e(TAG, e.toString())
        }
    }

    fun openCameraDocumentCNHFront(view: View){
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .setTheme(this.unicoTheme)
            .setTimeoutSession(this.timeout)
            .build()
            .prepareDocumentCamera(UnicoConfig(), this@MainActivity)

        documentType = DocumentType.CNH_FRENTE
    }

    fun openCameraDocumentCNHBack(view: View){
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .setTheme(this.unicoTheme)
            .setTimeoutSession(this.timeout)
            .build()
            .prepareDocumentCamera(UnicoConfig(), this@MainActivity)

        documentType = DocumentType.CNH_VERSO
    }

    override fun onErrorAcessoBio(p0: ErrorBio?) {
        var message = p0.toString()
        Log.e(TAG, message)
        textField.text = message
    }

    override fun onUserClosedCameraManually() {
        Log.d(TAG, "onUserClosedCameraManually")
        textField.text = "Camera fechada manualmente."
    }

    override fun onSystemClosedCameraTimeoutSession() {
        Log.d(TAG, "onSystemClosedCameraTimeoutSession")
        textField.text = "Tempo de sessao excedido."
    }

    override fun onSystemChangedTypeCameraTimeoutFaceInference() {
        Log.d(TAG, "onSystemChangedTypeCameraTimeoutFaceInference")
        textField.text = "Tempo de inferencia inteligente de face excedido."
    }

    override fun onSuccessSelfie(p0: ResultCamera?) {
        Log.d(TAG, "onSuccessSelfie")
        textField.text = "Selfie capturada com sucesso"
    }

    override fun onErrorSelfie(p0: ErrorBio?) {
        var message = p0.toString()
        Log.e(TAG, message)
        textField.text = message
    }

    override fun onCameraReady(p0: UnicoCheckCameraOpener.Document?) {
        p0?.open(documentType, this)
    }

    override fun onCameraFailed(p0: String?) {
        if (p0 != null) {
            Log.e(TAG, p0)
            textField.text = p0
        }
    }

    override fun onCameraReady(cameraOpener: UnicoCheckCameraOpener.Camera) {
        cameraOpener?.open(this)
        Log.d(TAG, "onCameraReady")
    }

    override fun onSuccessDocument(p0: ResultCamera?) {
        Log.d(TAG, "onSuccessDocument")
        textField.text = "Documento capturado com sucesso"
    }

    override fun onErrorDocument(p0: String?) {
        Log.e(TAG, p0.toString())
        textField.text = p0
    }
}