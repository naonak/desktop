package com.zaneschepke.wireguardautotunnel.core.ipc

import com.zaneschepke.wireguardautotunnel.core.crypto.Crypto
import com.zaneschepke.wireguardautotunnel.core.helper.PermissionsHelper
import java.io.File

object IPC {

    const val KEY_FILE = "ipc.key"
    const val USER_FOLDER = ".wgtunnel"
    const val SOCKET_FILE_NAME = "daemon.sock"

    // should be called by client ONLY
    fun getIPCSecret(): String {
        val ipcFile = File(System.getProperty("user.home"), "${IPC.USER_FOLDER}/${IPC.KEY_FILE}")
        if (!ipcFile.parentFile.exists()) ipcFile.parentFile.mkdirs()

        return if (!ipcFile.exists()) {
            val secret = Crypto.generateRandomBase64(32)
            ipcFile.writeText(secret)
            // Set 600 permissions immediately
            PermissionsHelper.setOwnerOnly(ipcFile.toPath())
            secret
        } else {
            ipcFile.readText()
        }
    }

    fun getIpcKeyPath(): String {
        val dir = File(System.getProperty("user.home"), USER_FOLDER)
        if (!dir.exists()) dir.mkdirs()
        val keyFile = File(dir, KEY_FILE)

        if (!keyFile.exists()) {
            val secret = Crypto.generateRandomBase64(32)
            keyFile.writeText(secret)
            PermissionsHelper.setOwnerOnly(keyFile.toPath())
        }
        return keyFile.canonicalPath
    }
}
