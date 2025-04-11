package com.unico.check_sdk_poc

import com.acesso.acessobio_android.onboarding.AcessoBioConfigDataSource

class UnicoConfig : AcessoBioConfigDataSource {

    override fun getBundleIdentifier(): String {
        return "com.unico.check_sdk_poc"
    }

    override fun getHostKey(): String {
        return "xxxxx"
    }

}