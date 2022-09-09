<p align='center'>
  <a href='https://unico.io'>
    <img width='350' src='https://unico.io/wp-content/uploads/2022/07/check.svg'></img>
  </a>
</p>

<h1 align='center'>SDK Android</h1>

<div align='center'>
  
  ### POC de implementação do SDK Android unico | check em Kotlin
  
  ![SDK](https://img.shields.io/badge/SDK-v4.1.5-blueviolet?logo=)
  ![ANDROID](https://img.shields.io/badge/Android-grey?logo=android)
</div>

## 💻 Compatibilidade

### Versões

- Versão mínima do Android 5.0 (API de nível 21)

### Dispositivos compatíveis

- Você pode conferior os aparelhos testados em nossos laboratórios <a href='https://developers.unico.io/guias/android/overview#disposit%C3%ADvos-compat%C3%ADveis'>nesta</a> lista de dispositivos.


## ✨ Como começar

### Ambiente de desenvolvimento & Credenciais Unico

- Primeiramente, você deve ter certeza que seu ambiente de desenvolvimento possuir o Android Studio (<a href='https://www.google.com/aclk?sa=l&ai=DChcSEwinnIeI4fH5AhX1QUgAHQeSBE4YABAAGgJjZQ&sig=AOD64_0aJo6DoyhwSY1Tw2aTGjg5R_0chw&q&adurl&ved=2ahUKEwiFiYCI4fH5AhW_IbkGHc1eDi0Q0Qx6BAgDEAE'>link</a>) instalado.
- Para utilizar nossos SDKs, você deve importar as credenciais unico (Client API Key) em seu projeto. Utilize <a href='https://developers.unico.io/guias/android/como-comecar#obtendo-suas-credenciais'>este</a> passo a passo para gerar as credenciais.

Depois de configurar a API Key e obter o bundle da aplicação Android com os dados do JSON, basta informá-los como parâmetros ao instanciar a classe `UnicoConfig`, que será utilizado posteriormente no método de preparação de câmera o ".prepareCamera()".

Segue o exemplo abaixo:

```
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
## 📦 Instalação

### Permissões para utilizar a câmera

Para utilizar o método de abertura de câmera é necessário adicionar as permissões antes de compilar a aplicação.

Insira as tags abaixo em:
- `android > app > src > main > AndroidManifest.xml`

```
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.INTERNET" />
```

### Inclusão da dependência

No arquivo app/build.gradle adicione a seguinte dependência:
```
implementation 'com.github.acesso-io:acessobio-android:<version>'
```
Em \<version\>  substitua pela versão mais atual da SDK Android.

## 📷 Captura de selfies

### 1️⃣ Inicializar nosso SDK

Crie uma instância do builder (gerado através da interface `IAcessoBioBuilder`) fornecendo como parâmetro o contexto em questão e a implementação da classe `AcessoBioListener`. Sobrescreva nossos métodos de callback com as lógicas de negócio de sua aplicação.

```
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

`onErrorAcessoBio(errorBio: ErrorBio?)`

Este método será invocado sempre quando qualquer erro de implementação ocorrer ao utilizar algum de nossos métodos recebendo um parâmetro do tipo <b>UnicoError</b> que contém detalhes do erro.

`onUserClosedCameraManually()`

Este método será invocado sempre quando o usuário fechar a câmera de forma manual, como por exemplo, ao clicar no botão "Voltar".

`onSystemClosedCameraTimeoutSession()`

Este método será invocado assim que o tempo máximo de sessão for atingido (Sem capturar nenhuma imagem).

O tempo máximo da sessão pode ser configurado em nosso <b>builder</b> através do método `setTimeoutSession`. Este método deve receber o tempo máximo da sessão em <b>segundos</b>.

`onSystemChangedTypeCameraTimeoutFaceInference()`

Este método será invocado assim que o tempo máximo para detecção da face de um usuário for atingido (sem ter nada detectado). Neste caso, o modo de câmera é alterado automaticamente para o modo manual (sem o smart frame).

<hr>

### <strong>❗ Todos os métodos acima devem ser criados da forma indicada em seu projeto (mesmo que sem nenhuma lógica). Caso contrário, o projeto não compilará com sucesso.</strong>

<hr>

### 2️⃣ Configurar modo da câmera
<p style='font-size: 15px'>
  <b>Modo inteligente (captura automática - Smart Camera)</b>
</p>

Por padrão, nosso SDK possui o enquadramento inteligente e a captura automática habilitados. Caso decida utilizar este modo de câmera, não será necessário alterar nenhuma configuração.

Caso as configurações da câmera tenham sido alteradas previamente em seu App, é possível restaurá-las através dos métodos `setAutoCapture` e `setSmartFrame`:

```
val unicoCheckCamera: UnicoCheckCamera = acessoBioBuilder
    .setAutoCapture(true)
    .setSmartFrame(true)
    .build()
```
<hr>

### <strong>❗ Não é possível implementar o método <span style='font-size: 15px'> `setAutoCapture(autoCapture: true)` </span> com o método <span style='font-size: 15px'> `setSmartFrame(smartFrame: false)`. </span>Ou seja, não é possível manter a captura automática sem o Smart Frame, pois ele é quem realiza o enquadramento inteligente. </strong>

<hr>

<p style='font-size: 15px'>
  <b>Modo normal</b>
</p>

Por padrão, nosso SDK possui o enquadramento inteligente e a captura automática habilitados. Neste caso, para utilizar o modo manual ambas configurações relacionadas a Smart Camera devem ser desligadas através dos métodos `setAutoCapture` e `setSmartFrame`:

```
val unicoCheckCamera: UnicoCheckCamera = acessoBioBuilder
    .setAutoCapture(false)
    .setSmartFrame(false)
    .build()
```

### 3️⃣ Customizar o frame de captura

<strong>Este passo é opcional, porém recomendado.</strong> Oferecemos a possibilidade de customização do frame de captura por meio do nosso SDK. Para customizar o frame, basta utilizar o método correspondente a propriedade a ser customizada, e posteriormente, aplicar o novo estilo através do método `setTheme()`. Para mais informações, consulte em nossa página de <a href='https://developers.unico.io/guias/android/referencias#customiza%C3%A7%C3%B5es'>Referências</a> do SDK. 

### 4️⃣ Efetuar abertura da câmera

Para informar ao método de abertura de câmera "o que fazer" deve ser implantado os <i>listeners</i> que serão chamados em situações de sucesso ou erro. A implementação desses métodos deverá ser feita através de uma instância de classe `UnicoSelfie`.

<p>

  <b style='font-size: 15px'> Método `onSuccessSelfie` </b>

</p>

Ao efetuar uma captura de imagem com sucesso, este método será invocado e retornará um objeto do tipo `ResultCamera` que será utilizado posteriormente na chamada de nossas APIs REST.

```
override fun onSuccessSelfie(p0: ResultCamera?) { }
```

<p>

  <b style='font-size: 15px'> Método `onErrorSelfie` </b>

</p>

Ao ocorrer algum erro na captura de imagem, este método será invocado e retornará um objeto do tipo `ErrorBio`.

```
override fun onErrorSelfie(p0: ErrorBio?) { }
```

<p>

  <b style='font-size: 15px'> Abrir câmera </b>

</p>

Devemos carregar a câmera utilizando o método `prepareSelfieCamera` e na sequência abrir com o método `open`. Exemplo abaixo:

```
fun openCameraSmart(view: View){
        AcessoBio(this, this)
            .setAutoCapture(true)
            .setSmartFrame(true)
            .build()
            .prepareSelfieCamera(UnicoConfig(), this@MainActivity)
    }

override fun onCameraReady(p0: UnicoCheckCameraOpener.Selfie?) {
        p0?.open(this)
        Log.d(TAG, "onCameraReady")
    }
```

Em caso de sucesso, o objeto `ResultCamera` do método `onSuccessSelfie` retornará 2 atributos: <strong> base64</strong> e <strong>encrypted</strong>.

#### - `base64`: pode ser utilizado caso queira exibir um preview da imagem em seu app;
#### - `encrypted`: deverá ser enviado na chamada de nossas APIs REST do <b>unico check</b>. Para mais informações detalhadas, visite nosso <a href='https://www3.acesso.io/identity/services/v3/docs/'>API Reference</a>.

## 📄 Captura de documentos

### 1️⃣ Inicializar nosso SDK

Na inicialização do SDK para captura de documentos são utilizadas exatamente os mesmos métodos <span style='font-size: 13px'>`onErrorUnico(UnicoError error), onUserClosedCameraManually(), onSystemClosedCameraTimeoutSession()`</span> e <span style='font-size: 13px'>`onSystemChangedTypeCameraTimeoutFaceInference()`</span> na [captura de selfie](#1️⃣-inicializar-nosso-sdk). 

### 2️⃣ Efetuar abertura de câmera

Para implementar os <i>listeners</i> para evento de câmera, o processo é exatamente igual a realizada na [captura de selfie](#4️⃣-efetuar-abertura-da-câmera). Porém, os métodos de callback de sucesso e erro são chamados desta forma: 
```
override fun onSuccessDocument(p0: ResultCamera?) {}
```
```
override fun onErrorDocument(p0: String?) {}
```

Finalmente, devemos abrir a câmera com as configurações feitas até aqui. Chamamos o método `prepareDocumentCamera` e na sequência o método `open`. Este método receberá os parâmetros abaixo:

<b style='font-size: 15px'>Tipos de documentos a serem capturados, sendo eles: </b>
- DocumentType.CNH: 
- DocumentType.CNH_FRENTE: 
- DocumentType.CNH_VERSO: 
- DocumentType.CPF: 
- DocumentType.RG_FRENTE: 
- DocumentType.RG_VERSO: 
- DocumentType.None: 

<b style='font-size: 15px'>Listeners configurados [acima](#2️⃣-efetuar-abertura-de-câmera)</b>

```
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

Em caso de sucesso, o objeto `ResultCamera` do método `onSuccessDocument` retornará 2 atributos (`base64` e `encrypted`) igualmente a [captura de selfie](#base64-pode-ser-utilizado-caso-queira-exibir-um-preview-da-imagem-em-seu-app).

### 3️⃣ Customizar o frame de captura

<strong>Este passo é opcional, porém recomendado.</strong> Oferecemos a possibilidade de customização do frame de captura por meio do nosso SDK. Para customizar o frame, basta utilizar o método correspondente a propriedade a ser customizada, e posteriormente, aplicar o novo estilo através do método `setTheme()`. Para mais informações, consulte em nossa página de <a href='https://developers.unico.io/guias/android/referencias#customiza%C3%A7%C3%B5es'>Referências</a> do SDK.

## 🤔 Dúvidas

Caso tenha alguma dúvida ou precise de ajuda com questões mais específicas, nossa <a href='https://developers.unico.io/guias/android/overview'>documentação</a> está disponível.
