package com.example.myapplication;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.security.cert.CertificateException;

import javax.net.ssl.SSLHandshakeException;
import javax.net.ssl.SSLPeerUnverifiedException;

import okhttp3.CertificatePinner;
import okhttp3.OkHttpClient;
import okhttp3.Request;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button = findViewById(R.id.button);
        button.setOnClickListener(this);
    }

    private void setText(String text) {
        runOnUiThread(() -> {
            TextView textView = findViewById(R.id.textView);
            textView.setText(text);
        });
    }

    @Override
    public void onClick(View v) {
        new Thread(() -> {
            String hostname = "www.baidu.com";
            CertificatePinner certificatePinner = new CertificatePinner.Builder()
                    .add(hostname, "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
                    .build();
            OkHttpClient client = new OkHttpClient.Builder()
                    .certificatePinner(certificatePinner)
                    .build();

            Request request = new Request.Builder()
                    .url("https://" + hostname)
                    .build();
            try {
                client.newCall(request).execute();
                setText("请求成功");

            }
            catch (SSLHandshakeException| SSLPeerUnverifiedException e){
                e.printStackTrace();
                setText("证书验证失败");
            }
            catch (IOException e) {
                e.printStackTrace();
                setText("请求失败");

            }
        }).start();
    }
}
