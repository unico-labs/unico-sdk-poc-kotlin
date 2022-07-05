package com.unico.check_sdk_poc

import com.acesso.acessobio_android.onboarding.AcessoBioConfigDataSource

class UnicoConfig : AcessoBioConfigDataSource{
    override fun getBundleIdentifier(): String {
        return ""
    }

    override fun getHostInfo(): String {
        return ""
    }

    override fun getHostKey(): String {
        return ""
    }

    override fun getMobileSdkAppId(): String {
        return ""
    }

    override fun getProjectId(): String {
        return ""
    }

    override fun getProjectNumber(): String {
        return ""
    }
}