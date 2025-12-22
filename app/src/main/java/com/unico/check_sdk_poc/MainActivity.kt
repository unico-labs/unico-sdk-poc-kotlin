package com.unico.check_sdk_poc

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.acesso.acessobio_android.*
import com.acesso.acessobio_android.onboarding.AcessoBio
import com.acesso.acessobio_android.onboarding.camera.CameraListener
import com.acesso.acessobio_android.onboarding.camera.UnicoCheckCameraOpener
import com.acesso.acessobio_android.onboarding.camera.document.DocumentCameraListener
import com.acesso.acessobio_android.onboarding.models.Environment
import com.acesso.acessobio_android.onboarding.types.DocumentType
import com.acesso.acessobio_android.services.dto.ErrorBio
import com.acesso.acessobio_android.services.dto.ResultCamera
import com.acesso.acessobio_android.services.dto.SuccessResult

class MainActivity : AppCompatActivity(),
    AcessoBioListener,
    iAcessoBioSelfie,
    CameraListener,
    iAcessoBioDocument,
    DocumentCameraListener {

    private lateinit var textField: TextView
    private lateinit var logTextView: TextView
    private lateinit var logScrollView: ScrollView
    private lateinit var documentType: DocumentType
    private val unicoTheme = UnicoTheme()
    private val timeout = 50.0
    private val CAMERA_PERMISSION_CODE = 1001
    private val TAG = "MainActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        textField = findViewById(R.id.mainText)
        logTextView = findViewById(R.id.logTextView)
        logScrollView = findViewById(R.id.logScrollView)

        findViewById<Button>(R.id.clearLogButton).setOnClickListener {
            logTextView.text = ""
            addLog("Log limpo.")
        }
    }

    private fun addLog(message: String) {
        runOnUiThread {

            logTextView.append("\n$message")
            logScrollView.post {
                logScrollView.fullScroll(View.FOCUS_DOWN)
            }
        }
        Log.d(TAG, message)
    }



    fun openCameraManual(view: View) {
        addLog("openCameraManual chamado")
        AcessoBio(this, this)
            .setAutoCapture(false)
            .setSmartFrame(false)
            .setTheme(unicoTheme)
            .setTimeoutSession(timeout)
            .setEnvironment(Environment.UAT)
            .build()
            .prepareCamera(UnicoConfig(), this)
    }

    fun openCameraSmart(view: View) {
        addLog("openCameraSmart chamado")
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .setTheme(unicoTheme)
            .setTimeoutSession(timeout)
            .setEnvironment(Environment.UAT)
            .build()
            .prepareCamera(UnicoConfig(), this)
    }

    fun openCameraLiveness(view: View) {
        addLog("openCameraLiveness chamado")
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            == PackageManager.PERMISSION_GRANTED) {
            startCameraLiveness()
        } else {
            addLog("Solicitando permissão de câmera...")
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.CAMERA),
                CAMERA_PERMISSION_CODE
            )
        }
    }

    private fun startCameraLiveness() {
        addLog("Permissão de câmera concedida. Iniciando SDK Liveness.")
        try {
            AcessoBio(this, this)
                .setTheme(unicoTheme)
                .setTimeoutSession(timeout)
                .setEnvironment(Environment.UAT)
                .build()
                .prepareCamera(UnicoConfig(), this)
        } catch (e: Exception) {
            addLog("Erro no startCameraLiveness: ${e.message}")
        }
    }

    fun openCameraDocumentCNHFront(view: View) {
        addLog("openCameraDocumentCNHFront chamado")
        documentType = DocumentType.CNH_FRENTE
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .setTheme(unicoTheme)
            .setTimeoutSession(timeout)
            .setEnvironment(Environment.UAT)
            .build()
            .prepareDocumentCamera(UnicoConfig(), this)
    }

    fun openCameraDocumentCNHBack(view: View) {
        addLog("openCameraDocumentCNHBack chamado")
        documentType = DocumentType.CNH_VERSO
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .setTheme(unicoTheme)
            .setTimeoutSession(timeout)
            .setEnvironment(Environment.UAT)
            .build()
            .prepareDocumentCamera(UnicoConfig(), this)
    }

    // Permissive
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == CAMERA_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                addLog("Permissão da câmera concedida.")
                startCameraLiveness()
            } else {
                addLog("Permissão da câmera negada pelo usuário.")
                Toast.makeText(this, "Permissão da câmera é obrigatória para continuar.", Toast.LENGTH_LONG).show()
            }
        }
    }

    // ----------- CALLBACKS SDK ------------
    override fun onErrorAcessoBio(error: ErrorBio?) {
        addLog("Erro AcessoBio: ${error.toString()}")
        textField.text = error.toString()
    }

    override fun onUserClosedCameraManually() {
        addLog("Usuário fechou a câmera manualmente.")
        textField.text = "Camera fechada manualmente."
    }

    override fun onSystemClosedCameraTimeoutSession() {
        addLog("Sessão encerrada por timeout.")
        textField.text = "Tempo de sessão excedido."
    }

    override fun onSystemChangedTypeCameraTimeoutFaceInference() {
        addLog("Timeout de inferência de face.")
        textField.text = "Tempo de inferência excedido."
    }

    override fun onSuccessSelfie(result: ResultCamera) {
        addLog("Selfie capturada com sucesso.")
        textField.text = "Selfie capturada com sucesso."

        addLog("JWT da selfie capturado com sucesso.")

         Log.d(TAG, "JWT COMPLETO DA SELFIE: ${result.encrypted}") // Descomente para depuração
    }

    override fun onErrorSelfie(error: ErrorBio?) {
        addLog("Erro na selfie: ${error.toString()}")
        textField.text = error.toString()
    }

    override fun onSuccess(result: SuccessResult) {
        addLog("Processo finalizado com sucesso.")
        textField.text = "Processo finalizado com sucesso."

        addLog("ProcessId: ${result.processId}")
        Log.d(TAG, "PROCESS ID: ${result.processId}")
    }

    override fun onCameraReady(document: UnicoCheckCameraOpener.Document?) {
        addLog("DocumentCamera pronto.")
        document?.open(documentType, this)
    }

    override fun onCameraReady(cameraOpener: UnicoCheckCameraOpener.Camera) {
        addLog("Camera pronta.")

        // SEM webAppToken 
        cameraOpener.open(this)

        // Token gerado pelo backend do cliente ao criar um processo
        // Retorna onSuccess(result: SuccessResult) com result.processId
        //cameraOpener.open(this, "webAppToken")
    }

    override fun onCameraFailed(error: String?) {
        addLog("Falha na câmera: $error")
        textField.text = error
    }

    override fun onSuccessDocument(result: ResultCamera?) {
        addLog("Documento capturado com sucesso.")
        textField.text = "Documento capturado com sucesso."
        result?.encrypted?.let {

            addLog("JWT do documento capturado com sucesso.")
            // Se precisar do valor do JWT para depuração, use Log.d(TAG, it) aqui.
             Log.d(TAG, "JWT COMPLETO DO DOCUMENTO: $it") // Descomente para depuração
        }
    }

    override fun onErrorDocument(error: String?) {
        addLog("Erro no documento: $error")
        textField.text = error
    }
}