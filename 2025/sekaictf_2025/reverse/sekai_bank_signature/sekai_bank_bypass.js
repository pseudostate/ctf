// frida -U -l <path>\sekai_bank_bypass.js -f com.sekai.bank
Java.perform(function() {
    let SignatureInterceptor = Java.use("com.sekai.bank.network.ApiClient$SignatureInterceptor");
    SignatureInterceptor["generateSignature"].implementation = function (request) {      
        var flagUrl = Java.use("okhttp3.HttpUrl").parse("https://sekaibank-api.chals.sekai.team/api/flag");
        var mediaType = Java.use("okhttp3.MediaType").parse("application/json; charset=utf-8");
        var flagBody = Java.use("okhttp3.RequestBody").create(mediaType, '{"unmask_flag":true}');
        var flagRequest = request.newBuilder().url(flagUrl).method("POST", flagBody).build();
        let result = this["generateSignature"](flagRequest);
        console.log(`Flag Signature = ${result}`);
        return result;
    };

    Java.use("com.android.org.conscrypt.TrustManagerImpl").checkTrustedRecursive.implementation = function (certs, authType, host, clientAuth, ocspData, tlsSctData) {
        return Java.use("java.util.ArrayList").$new();
    }; // SSL 인증 우회
});