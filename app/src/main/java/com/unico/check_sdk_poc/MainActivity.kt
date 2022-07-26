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
import com.acesso.acessobio_android.onboarding.camera.UnicoCheckCameraOpener
import com.acesso.acessobio_android.onboarding.camera.document.DocumentCameraListener
import com.acesso.acessobio_android.onboarding.camera.selfie.SelfieCameraListener
import com.acesso.acessobio_android.onboarding.types.DocumentType
import com.acesso.acessobio_android.services.dto.ErrorBio
import com.acesso.acessobio_android.services.dto.ResultCamera

var TAG = "MainActivity"

class MainActivity : AppCompatActivity(), AcessoBioListener, iAcessoBioSelfie, SelfieCameraListener,
    iAcessoBioDocument, DocumentCameraListener {

    lateinit var textField: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        textField = findViewById(R.id.mainText)
    }

    fun openCameraManual(view : View){
        AcessoBio(this, this)
            .setAutoCapture(false)
            .setSmartFrame(false)
            .build()
            .prepareSelfieCamera("unicoConfig.json", this@MainActivity)
    }

    fun openCameraSmart(view: View){
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .build()
            .prepareSelfieCamera("unicoConfig.json", this@MainActivity)
}

    fun openCameraLiveness(view: View){
        AcessoBio(this, this)
            .build()
            .prepareSelfieCamera("unicoConfigLiveness.json", this@MainActivity)
    }

    fun openCameraDocument(view: View){
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .build()
            .prepareDocumentCamera("unicoConfig.json", this@MainActivity)
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

    override fun onCameraReady(p0: UnicoCheckCameraOpener.Selfie?) {
        p0?.open(this)
        Log.d(TAG, "onCameraReady")
    }

    override fun onCameraReady(p0: UnicoCheckCameraOpener.Document?) {
        p0?.open(DocumentType.CNH, this)
    }

    override fun onCameraFailed(p0: String?) {
        if (p0 != null) {
            Log.e(TAG, p0)
            textField.text = p0
        }
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