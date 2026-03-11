'use strict';

function log(x) {
    console.log(x);
}

function findExport(name) {
    try {
        return Module.findExportByName(null, name);
    } catch (e) {
        return null;
    }
}
var LIBSEC_PATH_1 = "/data/data/kr.co.eqst.aos/cache/libsec.so";
var LIBSEC_PATH_2 = "/data/user/0/kr.co.eqst.aos/cache/libsec.so";

function isLibsecPath(p) {
    if (!p) return false;
    return p.indexOf(LIBSEC_PATH_1) !== -1 || p.indexOf(LIBSEC_PATH_2) !== -1;
}

function isSuPath(p) {
    if (!p) return false;
    p = p.toLowerCase();
    return (p.indexOf("/system/xbin/su") !== -1 || p.indexOf("/system/bin/su") !== -1 || p.indexOf("/sbin/su") !== -1 || p.indexOf("/system/sd/xbin/su") !== -1 || p.indexOf("/data/local/xbin/su") !== -1 || p.indexOf("/data/local/bin/su") !== -1 || p.indexOf("/data/local/su") !== -1 || p.indexOf("/su/bin/su") !== -1);
}

function installNativeHooks() {
    function hookPathFunc(name) {
        var p = findExport(name);
        if (!p) return;
        Interceptor.attach(p, {
            onEnter: function(args) {
                this.path = null;
                try {
                    this.path = Memory.readCString(args[0]);
                } catch (e) {}
            },
            onLeave: function(retval) {
                if (!this.path) return;
                if (isSuPath(this.path)) {
                    log("[*] " + name + " bypass: " + this.path);
                    retval.replace(ptr(-1));
                    return;
                }
                if (this.path.indexOf("/proc/self/maps") !== -1) {
                    log("[*] " + name + " observe maps: " + this.path);
                }
                if (isLibsecPath(this.path)) {
                    log("[*] " + name + " observe libsec: " + this.path + " => " + retval);
                }
            }
        });
        log("[*] hooked " + name);
    }
    hookPathFunc("access");
    hookPathFunc("stat");
    hookPathFunc("stat64");
    hookPathFunc("open");
    hookPathFunc("openat");
    hookPathFunc("fopen");
    var geteuidPtr = findExport("geteuid");
    if (geteuidPtr) {
        Interceptor.replace(geteuidPtr, new NativeCallback(function() {
            log("[*] geteuid bypass -> 2000");
            return 2000;
        }, 'uint', []));
        log("[*] replaced geteuid");
    }

    function replaceVoid(name, argTypes) {
        var p = findExport(name);
        if (!p) return;
        Interceptor.replace(p, new NativeCallback(function() {
            log("[*] " + name + " blocked");
        }, 'void', argTypes));
        log("[*] replaced " + name);
    }

    function replaceInt(name, argTypes, ret) {
        var p = findExport(name);
        if (!p) return;
        Interceptor.replace(p, new NativeCallback(function() {
            log("[*] " + name + " blocked");
            return ret;
        }, 'int', argTypes));
        log("[*] replaced " + name);
    }
    replaceInt("kill", ['int', 'int'], 0);
    replaceInt("tgkill", ['int', 'int', 'int'], 0);
    replaceInt("raise", ['int'], 0);
    replaceVoid("abort", []);
    replaceVoid("exit", ['int']);
    replaceVoid("_exit", ['int']);
    var unlinkPtr = findExport("unlink");
    if (unlinkPtr) {
        Interceptor.replace(unlinkPtr, new NativeCallback(function(pathPtr) {
            var path = "";
            try {
                path = Memory.readCString(pathPtr);
            } catch (e) {}
            if (isLibsecPath(path)) {
                log("[*] unlink blocked for libsec: " + path);
                return 0;
            }
            var realUnlink = new NativeFunction(unlinkPtr, 'int', ['pointer']);
            return realUnlink(pathPtr);
        }, 'int', ['pointer']));
        log("[*] hooked unlink");
    }

    function hookDlopen(name) {
        var p = findExport(name);
        if (!p) return;
        Interceptor.attach(p, {
            onEnter: function(args) {
                this.path = null;
                try {
                    this.path = Memory.readCString(args[0]);
                } catch (e) {}
                if (this.path) {
                    if (this.path.indexOf("libfir-lib-arm64-v8a.so") !== -1 || this.path.indexOf("libsec.so") !== -1) {
                        log("[*] " + name + ": " + this.path);
                    }
                }
            },
            onLeave: function(retval) {
                if (this.path && isLibsecPath(this.path)) {
                    log("[*] libsec dlopen result: " + retval);
                }
            }
        });
        log("[*] hooked " + name);
    }
    hookDlopen("dlopen");
    hookDlopen("android_dlopen_ext");
}

function installJavaHooks() {
    Java.perform(function() {
        log("[*] Java.perform entered");
        try {
            var System = Java.use("java.lang.System");
            System.exit.overload('int').implementation = function(code) {
                log("[*] System.exit blocked: " + code);
            };
            log("[*] Java exit hooks installed");
        } catch (e) {
            log("[*] Java exit hook failed: " + e);
        }
        try {
            var Process = Java.use("android.os.Process");
            Process.killProcess.overload('int').implementation = function(pid) {
                log("[*] Process.killProcess blocked: " + pid);
            };
            log("[*] android.os.Process.killProcess hook installed");
        } catch (e) {
            log("[*] killProcess hook failed: " + e);
        }
        try {
            var Intrinsics = Java.use("kotlin.jvm.internal.Intrinsics");
            Intrinsics.areEqual.overload('java.lang.Object', 'java.lang.Object').implementation = function(a, b) {
                var s1 = "";
                var s2 = "";
                try {
                    s1 = a ? a.toString() : "null";
                } catch (e) {}
                try {
                    s2 = b ? b.toString() : "null";
                } catch (e) {}
                if (s1 === "welcome to EQST CTF" && s2 === "welcome to EQST CTF") {
                    log("[*] welcome to EQST CTF bypass");
                    return false;
                }
                return this.areEqual(a, b);
            };
            log("[*] Intrinsics.areEqual hook installed");
        } catch (e) {
            log("[*] Intrinsics.areEqual hook failed: " + e);
        }
        try {
            var Splash = Java.use("kr.co.eqst.aos.SplashActivity");
            Splash.g0.overload('java.lang.String', 'java.lang.String').implementation = function(a, b) {
                log("[*] g0 bypass");
                return true;
            };
            Splash.k0.overload().implementation = function() {
                log("[*] k0 bypass");
                return false;
            };
            Splash.l0.overload().implementation = function() {
                log("[*] l0 bypass");
                return false;
            };
            Splash.h0.overload().implementation = function() {
                log("[*] h0 bypass");
                return false;
            };
            log("[*] SplashActivity hooks installed");
        } catch (e) {
            log("[*] SplashActivity hook failed: " + e);
        }
        try {
            var MainActivity = Java.use("kr.co.eqst.aos.MainActivity");
            if (MainActivity.showflag) {
                MainActivity.showflag.implementation = function() {
                    log("[*] MainActivity.showflag called");
                    return this.showflag();
                };
                log("[*] MainActivity.showflag hook installed");
            }
        } catch (e) {
            log("[*] MainActivity.showflag hook failed: " + e);
        }
        setTimeout(function() {
            Java.perform(function() {
                try {
                    Java.enumerateClassLoaders({
                        onMatch: function(loader) {
                            try {
                                var cf = Java.ClassFactory.get(loader);
                                try {
                                    var AssetUtils = cf.use("kr.co.eqst.aos.AssetUtils");
                                    log("[*] AssetUtils visible via loader: " + loader);
                                } catch (e) {}
                            } catch (e) {}
                        },
                        onComplete: function() {
                            log("[*] enumerateClassLoaders done");
                        }
                    });
                } catch (e) {
                    log("[*] enumerateClassLoaders failed: " + e);
                }
            });
        }, 1000);
    });
}

function log(x) {
    console.log(x);
}

function find(name) {
    try {
        return Module.findExportByName(null, name);
    } catch (e) {
        return null;
    }
}
var trackedFds = {};

function installDumpHooks() {
    var memfdCreate = find("memfd_create");
    if (memfdCreate) {
        Interceptor.attach(memfdCreate, {
            onEnter: function(args) {
                this.name = "";
                try {
                    this.name = Memory.readCString(args[0]);
                } catch (e) {}
            },
            onLeave: function(retval) {
                var fd = retval.toInt32();
                if (this.name.indexOf("libthird") !== -1 && fd >= 0) {
                    trackedFds[fd] = {
                        name: this.name,
                        total: 0
                    };
                    log("[*] memfd_create tracked fd=" + fd + " name=" + this.name);
                }
            }
        });
    }
    var writePtr = find("write");
    if (writePtr) {
        Interceptor.attach(writePtr, {
            onEnter: function(args) {
                this.fd = args[0].toInt32();
                this.buf = args[1];
                this.count = args[2].toInt32();
            },
            onLeave: function(retval) {
                if (!trackedFds.hasOwnProperty(this.fd)) return;
                if (this.count <= 0) return;
                try {
                    var data = Memory.readByteArray(this.buf, this.count);
                    var path = "/data/local/tmp/libthird_dump_" + this.fd + "_" + trackedFds[this.fd].total + ".bin";
                    var f = new File(path, "wb");
                    f.write(data);
                    f.flush();
                    f.close();
                    trackedFds[this.fd].total += this.count;
                    log("[*] dumped chunk fd=" + this.fd + " size=" + this.count + " -> " + path);
                } catch (e) {
                    log("[*] write dump failed: " + e);
                }
            }
        });
    }
    var androidDlopenExt = find("android_dlopen_ext");
    if (androidDlopenExt) {
        Interceptor.attach(androidDlopenExt, {
            onEnter: function(args) {
                this.path = "";
                try {
                    this.path = Memory.readCString(args[0]);
                } catch (e) {}
                if (this.path.indexOf("libthird.so") !== -1) {
                    log("[*] android_dlopen_ext: " + this.path);
                }
            }
        });
    }
}

function installAntiAntiFrida() {
    var strstrPtr = find("strstr");
    if (strstrPtr) {
        Interceptor.attach(strstrPtr, {
            onEnter: function(args) {
                this.h = null;
                this.n = null;
                try {
                    this.h = Memory.readCString(args[0]);
                } catch (e) {}
                try {
                    this.n = Memory.readCString(args[1]);
                } catch (e) {}
            },
            onLeave: function(retval) {
                try {
                    if (!this.h || !this.n) return;
                    var hay = this.h.toLowerCase();
                    var nee = this.n.toLowerCase();
                    var badNeedle = nee === "frida" || nee === "gadget" || nee === "libfrida" || nee === "re.frida.server";
                    if (badNeedle && hay.indexOf(".so") !== -1) {
                        retval.replace(ptr(0));
                    }
                } catch (e) {}
            }
        });
    }
    var connectPtr = find("connect");
    if (connectPtr) {
        Interceptor.attach(connectPtr, {
            onEnter: function(args) {
                this.block = false;
                try {
                    var sa = args[1];
                    var family = Memory.readU16(sa);
                    if (family === 2) {
                        var port_be = Memory.readU16(sa.add(2));
                        var port = ((port_be & 0xff) << 8) | ((port_be >> 8) & 0xff);
                        var ip = Memory.readU8(sa.add(4)) + "." + Memory.readU8(sa.add(5)) + "." + Memory.readU8(sa.add(6)) + "." + Memory.readU8(sa.add(7));
                        if (ip === "127.0.0.1" && (port === 27042 || port === 27043)) {
                            this.block = true;
                            log("[*] blocked frida port connect " + ip + ":" + port);
                        }
                    }
                } catch (e) {}
            },
            onLeave: function(retval) {
                if (this.block) {
                    retval.replace(ptr(-1));
                }
            }
        });
    }
}
setImmediate(function() {
    installNativeHooks();
    installJavaHooks();
    installAntiAntiFrida();
    installDumpHooks();
});