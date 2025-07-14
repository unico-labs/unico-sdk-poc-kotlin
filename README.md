<p align="center">
  <a href="https://unico.io">
    <img width="350" src="https://unico.io/wp-content/uploads/2024/05/idcloud-horizontal-color.svg">
  </a>
</p>

<h1 align="center">SDK Android</h1>

<div align="center">
  
### POC de implementação do SDK Android Unico | Check em Kotlin
  
![ANDROID](https://img.shields.io/badge/Android-grey?logo=android)
</div>

---

## 💻 Compatibilidade

### 📌 Versões Mínimas

- **Android:** 5.0 (API nível 21)
- **Kotlin:** 1.6

### 📱 Dispositivos Compatíveis

Você pode conferir os aparelhos testados em nossos laboratórios nesta [lista de dispositivos](https://developers.unico.io/guias/android/overview#disposit%C3%ADvos-compat%C3%ADveis).

---

## ✨ Em caso de algum conflito de biblioteca com nossa SDK o caminho correto é sempre abrir um chamado em nossa plataforma oficial para o nosso time de Suporte.

---

## ✨ Como Começar

### 🚀 Ambiente de Desenvolvimento & Credenciais Unico

- **Android Studio:** Certifique-se de ter o [Android Studio](https://www.google.com/aclk?sa=l&ai=DChcSEwinnIeI4fH5AhX1QUgAHQeSBE4YABAAGgJjZQ&sig=AOD64_0aJo6DoyhwSY1Tw2aTGjg5R_0chw&q&adurl&ved=2ahUKEwiFiYCI4fH5AhW_IbkGHc1eDi0Q0Qx6BAgDEAE) instalado.
- **Credenciais Unico:** Para utilizar nossos SDKs, você deve importar as credenciais Unico (Client API Key) em seu projeto. Siga [este passo a passo](https://developers.unico.io/guias/android/como-comecar#obtendo-suas-credenciais) para gerar as credenciais.

Após configurar a API Key e obter o bundle da aplicação Android com os dados do JSON, informe-os como parâmetros ao instanciar a classe `UnicoConfig`, que será utilizada posteriormente no método de preparação da câmera, o `prepareCamera()`.

Exemplo:

```kotlin
package <package_name>

import com.acesso.acessobio_android.onboarding.AcessoBioConfigDataSource

class UnicoConfig : AcessoBioConfigDataSource {
    override fun getProjectNumber(): String {
        return PROJECT_NUMBER
    }

    override fun getProjectId(): String {
        return PROJECT_ID
    }

    override fun getMobileSdkAppId(): String {
        return MOBILE_SDK_APP_ID
    }

    override fun getBundleIdentifier(): String {
        return BUNDLE_IDENTIFIER
    }

    override fun getHostInfo(): String {
        return HOST_INFO
    }

    override fun getHostKey(): String {
        return HOST_KEY
    }
}
```

---

## 📦 Instalação

### 🔒 Permissões para Utilizar a Câmera

Antes de compilar a aplicação, adicione as seguintes permissões no arquivo:
`android > app > src > main > AndroidManifest.xml`

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.INTERNET" />
```

### 📥 Inclusão da Dependência

No arquivo `app/build.gradle`, adicione a seguinte dependência:

```gradle
implementation 'com.github.acesso-io:acessobio-android:<version>'
```

Substitua `<version>` pela versão mais atual da SDK Android.

---

## 📷 Captura de Selfies

### 1️⃣ Inicializar o SDK

Crie uma instância do builder (gerado através da interface `IAcessoBioBuilder`), fornecendo como parâmetros o contexto atual e a implementação da classe `AcessoBioListener`. Sobrescreva os métodos de callback com a lógica de negócio da sua aplicação:

```kotlin
internal class MainActivity : AppCompatActivity() {

    private val callback = object : AcessoBioListener {
        override fun onErrorAcessoBio(errorBio: ErrorBio?) { }
    
        override fun onUserClosedCameraManually() { }
    
        override fun onSystemClosedCameraTimeoutSession() { }
    
        override fun onSystemChangedTypeCameraTimeoutFaceInference() { }
    }

    private val acessoBioBuilder: IAcessoBioBuilder = AcessoBio(this, callback)
}
```

> **Detalhes dos Callbacks:**
>
> - **`onErrorAcessoBio(errorBio: ErrorBio?)`:** Invocado sempre que ocorrer um erro de implementação, retornando um objeto do tipo `UnicoError` com detalhes do erro.
> - **`onUserClosedCameraManually()`:** Chamado quando o usuário fecha a câmera manualmente (por exemplo, ao clicar no botão "Voltar").
> - **`onSystemClosedCameraTimeoutSession()`:** Invocado quando o tempo máximo de sessão é atingido sem capturar nenhuma imagem. (*Nota:* O tempo máximo pode ser configurado via `setTimeoutSession`, que recebe o valor em segundos.)
> - **`onSystemChangedTypeCameraTimeoutFaceInference()`:** Chamado quando o tempo máximo para detecção da face do usuário é atingido (nenhuma face detectada), alterando automaticamente para o modo manual (sem Smart Frame).
>
> **❗ Importante:** Todos os métodos acima devem ser implementados conforme indicado. A ausência de algum deles pode impedir a compilação do projeto.

---

### 2️⃣ Configurar o Modo da Câmera

#### 🔄 Modo Inteligente (Captura Automática - Smart Camera)

Por padrão, o SDK possui enquadramento inteligente e captura automática habilitados. Se optar por esse modo, nenhuma configuração adicional é necessária.  
Caso as configurações da câmera tenham sido alteradas previamente, restaure-as utilizando os métodos `setAutoCapture` e `setSmartFrame`:

```kotlin
val unicoCheckCamera: UnicoCheckCamera = acessoBioBuilder
    .setAutoCapture(true)
    .setSmartFrame(true)
    .build()
```

> **❗ Atenção:** Não é possível usar `setAutoCapture(true)` com `setSmartFrame(false)`. Ou seja, não é possível manter a captura automática sem o Smart Frame, que é responsável pelo enquadramento inteligente.

#### 🔄 Modo Normal

Para utilizar o modo manual, desative as configurações do Smart Camera:

```kotlin
val unicoCheckCamera: UnicoCheckCamera = acessoBioBuilder
    .setAutoCapture(false)
    .setSmartFrame(false)
    .build()
```

---

### 3️⃣ Customizar o Frame de Captura

**Opcional, mas recomendado.**  
Você pode customizar o frame de captura utilizando o método correspondente à propriedade desejada e, em seguida, aplicar o novo estilo com o método `setTheme()`.  
Para mais informações, consulte as [Referências do SDK](https://developers.unico.io/guias/android/referencias#customiza%C3%A7%C3%B5es).

---

### 4️⃣ Efetuar a Abertura da Câmera

Implemente os _listeners_ para tratar os eventos de sucesso ou erro ao abrir a câmera. Essa implementação é realizada através de uma instância da classe `UnicoSelfie`.

- **Método `onSuccessSelfie`:**  
  Chamado ao capturar uma imagem com sucesso, retornando um objeto do tipo `ResultCamera` que será utilizado posteriormente nas chamadas das APIs REST.

  ```kotlin
  override fun onSuccessSelfie(p0: ResultCamera?) { }
  ```

- **Método `onErrorSelfie`:**  
  Invocado quando ocorre um erro na captura de imagem, retornando um objeto do tipo `ErrorBio`.

  ```kotlin
  override fun onErrorSelfie(p0: ErrorBio?) { }
  ```

**Abrindo a Câmera:**

Utilize o método `prepareCamera` para carregar a câmera e, em seguida, abra-a com o método `open`. Exemplo:

```kotlin
fun openCameraSmart(view: View){
    AcessoBio(this, this)
        .setAutoCapture(true)
        .setSmartFrame(true)
        .build()
        .prepareCamera(UnicoConfig(), this@MainActivity)
}

override fun onCameraReady(p0: UnicoCheckCameraOpener.Camera?) {
    p0?.open(this)
    Log.d(TAG, "onCameraReady")
}
```

> **Observação:** Em caso de sucesso, o objeto `ResultCamera` retornado pelo método `onSuccessSelfie` fornecerá os atributos **base64** e **encrypted**.
>
> - **base64:** Pode ser utilizado para exibir um preview da imagem no seu app.
> - **encrypted:** Deve ser enviado na chamada das APIs REST do Unico Check. Para mais detalhes, consulte nossa [API Reference](https://www3.acesso.io/identity/services/v3/docs/).

---

## 📄 Captura de Documentos

### 1️⃣ Inicializar o SDK

A inicialização do SDK para captura de documentos utiliza os mesmos métodos de callback da captura de selfie:  
`onErrorUnico(UnicoError error)`, `onUserClosedCameraManually()`, `onSystemClosedCameraTimeoutSession()` e `onSystemChangedTypeCameraTimeoutFaceInference()`.

---

### 2️⃣ Efetuar a Abertura da Câmera

A configuração dos _listeners_ para os eventos da câmera é idêntica à realizada na captura de selfie, porém os métodos de callback de sucesso e erro são:

```kotlin
override fun onSuccessDocument(p0: ResultCamera?) { }
```

```kotlin
override fun onErrorDocument(p0: String?) { }
```

Abra a câmera com as configurações definidas utilizando o método `prepareDocumentCamera` seguido de `open`. Esse método recebe os seguintes parâmetros:

- **Tipos de Documentos a Capturar:**
  - `DocumentType.CNH`
  - `DocumentType.CNH_FRENTE`
  - `DocumentType.CNH_VERSO`
  - `DocumentType.CPF`
  - `DocumentType.RG_FRENTE`
  - `DocumentType.RG_VERSO`
  - `DocumentType.None`

- **Listeners:** Conforme configurados anteriormente.

Exemplo:

```kotlin
fun openCameraDocument(view: View){
    AcessoBio(this, this)
        .setAutoCapture(true)
        .setSmartFrame(true)
        .build()
        .prepareDocumentCamera(UnicoConfig(), this@MainActivity)
}

override fun onCameraReady(p0: UnicoCheckCameraOpener.Document?) {
    p0?.open(DocumentType.CNH, this)
}
```

> **Observação:** Em caso de sucesso, o objeto `ResultCamera` retornado pelo método `onSuccessDocument` fornecerá os atributos **base64** e **encrypted**, assim como na captura de selfie.

---

### 3️⃣ Customizar o Frame de Captura

**Opcional, mas recomendado.**  
Você pode customizar o frame de captura utilizando o método correspondente e aplicar o novo estilo através do método `setTheme()`.  
Para mais informações, consulte as [Referências do SDK](https://developers.unico.io/guias/android/referencias#customiza%C3%A7%C3%B5es).

---

## 🤔 Dúvidas

Se você tiver alguma dúvida ou precisar de ajuda com questões específicas, nossa [documentação](https://developers.unico.io/guias/android/overview) está à disposição.
