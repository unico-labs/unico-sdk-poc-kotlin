package com.unico.check_sdk_poc

import android.app.Activity
import android.app.AlertDialog

class LoadingDialog(myActivity: Activity) {

    var acitivity = myActivity;
    lateinit var dialog: AlertDialog;


    fun startLoading(){
        var builder = AlertDialog.Builder(acitivity);
        var inflater = acitivity.layoutInflater;

        builder
            .setView(inflater.inflate(R.layout.loading_dialog, null))
            .setCancelable(false);

        dialog = builder.create();
        dialog.show();
    }

    fun dismissLoading(){
        dialog.dismiss();
    }
}