const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM();  // 这里应填入原来的HTML，但其实这段代码并没有使用到那上面的内容，所以弄个空dom也行
window = dom.window;
document = window.document;
window.decodeURIComponent = decodeURIComponent;

(function (uH_) {
    function KI_() {
        Ks_();
    }

    function jE_() {
        let a = '' + Rl_ + TP_ + zj_ + he_ + Mk_ + nu_ + kv_ + ae_ + LE_ + oT_ + SJ_ + Pr_ + gF_ + rs_ + YM_ + RN_ + nV_ + iV_;
        let b = AQ_ + bR_ + aK_ + AQ_ + ax_ + Az_ + AQ_ + ct_ + XH_ + AQ_ + bR_ + aK_ + AQ_ + Bj_ + le_ + AQ_ + DQ_ + AI_ + AQ_ + bR_ + Bj_ + AQ_ + Bj_ + Sg_ + AQ_ + ct_ + AF_ + AQ_ + bR_ + fH_ + AQ_ + ax_ + ax_ + AQ_ + ct_ + aU_ + AQ_ + bR_ + ax_ + AQ_ + Bj_ + Bj_ + AQ_ + ct_ + DQ_ + AQ_ + bR_ + aQ_ + AQ_ + DQ_ + XH_ + AQ_ + ct_ + Az_ + AQ_ + bR_ + aK_ + AQ_ + ax_ + ct_ + AQ_ + ax_ + AI_ + AQ_ + bR_ + le_ + AQ_ + ax_ + ax_ + AQ_ + Bj_ + DQ_ + AQ_ + bR_ + ax_ + AQ_ + ct_ + XH_ + AQ_ + Bj_ + le_ + AQ_ + bR_ + fH_ + AQ_ + ct_ + fH_ + AQ_ + Bj_ + Az_;
        vz_ = uc_()[a](b);
        ti_ = Er_((DU_ + Az_ + ax_ + aK_ + fH_ + AF_ + le_ + AI_ + Bj_ + aQ_), KM_(''));
        SE_ = Er_(('' + KM_(';')), Ep_(';'));
        KI_();
        return ';';
    }

    var SE_ = '';
    var ti_ = '';
    var vz_ = '';
    var kj_ = uH_.createElement('style');
    if (uH_.head) {
        uH_.head.appendChild(kj_);
    } else {
        uH_.getElementsByTagName('head')[0].appendChild(kj_);
    }
    var ee_ = kj_.sheet;

    function CH_() {
        if (ee_ !== undefined && ee_['' + KL_ + Ro_ + up_ + ov_ + Ys_ + dZ_ + DB_ + AC_ + Za_ + YB_]) {
            return true;
        } else {
            return false;
        }
    }

    function Ks_() {
        for (QG_ = 0; QG_ < ti_.length; QG_++) {
            var NL_ = Er_(ti_[QG_], ',');
            var YO_ = '';
            for (BC_ = 0; BC_ < NL_.length; BC_++) {
                YO_ += BD_(QG_) + '';
            }
            Je_(NL_[0], YO_);
        }
    }

    function Je_(QG_, zO_) {
        let a = '' + KL_ + Ro_ + up_ + ov_ + Ys_ + dZ_ + DB_ + AC_ + Za_ + YB_;
        ee_[a](pu_(QG_) + TU_() + '"' + zO_ + '" }', 0);
        var NL_ = kX_(pu_(QG_));
        for (x in NL_) {
            try {
                NL_[x].currentStyle = '';
            } catch (e) {
            }
        }
    }

    function pu_(QG_) {
        return '.code1' + QG_ + '';
    }

    function TU_() {
        return '::before { content:'
    }


    function gK_() {
        var yF_ = '';
        try {
            if (HS_GetCustomStyle) {
                yF_ = HS_GetCustomStyle();
            } else {
                if (navigator.userAgent.indexOf('Windows NT 5') != -1) {
                    yF_ = 'margin-bottom:-4.8px;';
                } else {
                    yF_ = 'margin-bottom:-5px;';
                }
            }
        } catch (e) {
        }
        return yF_;
    }

    function kY_(zO_, QG_) {
        var NL_ = kX_(pu_(zO_));
        for (x in NL_) {
            NL_[x].innerHTML = QG_;
            try {
                NL_[x].currentStyle = '';
            } catch (e) {
            }
        }
    }

    function kX_(zO_) {
        return document.querySelectorAll(zO_);
    }

    function Er_(zO_, QG_) {
        if (zO_) {
            let a = '' + Xf_ + xj_ + DA_ + xq_ + bT_;
            return zO_[a](QG_);
        } else {
            return '';
        }
    }

    function BD_(zO_) {
        let a = '' + OX_ + fj_ + mH_ + wi_ + PT_ + ro_;
        return vz_[a](parseInt(zO_));
    }

    function KM_(zO_) {
        tu_();
        if (Ij_()) {
            Ij_()['' + tc_ + Sb_ + Be_ + Ny_ + UQ_ + cv_ + Ar_ + Iq_ + PQ_ + FM_ + ua_ + IA_ + Gz_ + jS_ + bG_ + TR_] = function (element, pseudoElt) {
                if (pseudoElt != undefined && typeof (pseudoElt) == 'string' && pseudoElt.toLowerCase().indexOf(':before') > -1) {
                    var obj = {};
                    obj.getPropertyValue = function (x) {
                        return x;
                    };
                    return obj;
                } else {
                    return window.hs_fuckyou_dd(element, pseudoElt);
                }
            };
        }
        return zO_;
    }

    function Ep_(zO_) {
        tu_();
        uc_()['' + tc_ + Sb_ + Be_ + Ny_ + UQ_ + cv_ + Ar_ + Iq_ + PQ_ + FM_ + ua_ + IA_ + Gz_ + jS_ + bG_ + TR_] = function (element, pseudoElt) {
            if (pseudoElt != undefined && typeof (pseudoElt) == 'string' && pseudoElt.toLowerCase().indexOf(':before') > -1) {
                var obj = {};
                obj.getPropertyValue = function (x) {
                    return x;
                };
                return obj;
            } else {
                return window.hs_fuckyou(element, pseudoElt);
            }
        };
        return zO_;
    }

    function Ij_() {
        return uH_['' + OL_ + ss_ + xV_ + mo_ + fd_ + Lq_ + sE_ + Gc_ + Uu_ + nX_ + or_];
    }

    function uc_() {
        let a = '' + fY_ + kC_ + DZ_ + FD_ + ir_ + Yq_;
        return this[a];
    }

    function KA_() {
        return uc_()['' + Gk_ + St_ + Ex_ + OS_ + mx_ + ci_ + aj_ + pd_]['' + oc_ + UD_ + Oe_ + jv_];
    }

    function tu_() {
        if (window.hs_fuckyou == undefined) {
            window.hs_fuckyou = uc_()['' + tc_ + Sb_ + Be_ + Ny_ + UQ_ + cv_ + Ar_ + Iq_ + PQ_ + FM_ + ua_ + IA_ + Gz_ + jS_ + bG_ + TR_];
        }
        if (Ij_()) {
            if (window.hs_fuckyou_dd == undefined) {
                window.hs_fuckyou_dd = Ij_()['' + tc_ + Sb_ + Be_ + Ny_ + UQ_ + cv_ + Ar_ + Iq_ + PQ_ + FM_ + ua_ + IA_ + Gz_ + jS_ + bG_ + TR_];
            }
        }
    }

    function Yj_() {
        return '';
    }

    var AC_ = 'u';
    var ae_ = 'R';
    var AF_ = '2';
    var AI_ = '0';
    var aj_ = 'o';
    var aK_ = '6';
    var AQ_ = '%';
    var aQ_ = '4';
    var Ar_ = 'p';
    var aU_ = 'C';
    var ax_ = '8';
    var Az_ = '1';
    var Be_ = 't';
    var bG_ = 'l';
    var bJ_ = '8';
    var Bj_ = '9';
    var bq_ = '0';
    var bR_ = 'E';
    var bT_ = 't';
    var cB_ = '8';
    var ci_ = 'i';
    var CJ_ = '0';
    var cl_ = '8';
    var ct_ = 'A';
    var cv_ = 'm';
    var DA_ = 'l';
    var DB_ = 'R';
    var di_ = '4';
    var DL_ = '9';
    var Dp_ = '8';
    var DQ_ = 'B';
    var du_ = '%';
    var DU_ = '3';
    var DZ_ = 'n';
    var dZ_ = 't';
    var Ex_ = 'c';
    var FD_ = 'd';
    var fd_ = 'u';
    var fF_ = 't';
    var fH_ = '7';
    var fj_ = 'h';
    var FM_ = 'e';
    var Fp_ = 'r';
    var ft_ = '4';
    var FV_ = 'a';
    var fY_ = 'w';
    var Fz_ = '%';
    var Gc_ = 'V';
    var gF_ = 'p';
    var Gk_ = 'l';
    var gl_ = 'o';
    var gZ_ = '4';
    var Gz_ = 't';
    var Hb_ = '%';
    var hC_ = '%';
    var HD_ = '%';
    var he_ = 'o';
    var HN_ = 'B';
    var HP_ = 'E';
    var hq_ = '1';
    var hR_ = 'C';
    var HZ_ = '%';
    var IA_ = 'S';
    var ID_ = '9';
    var id_ = 'l';
    var ig_ = '%';
    var Ig_ = '%';
    var In_ = '9';
    var Io_ = '%';
    var Iq_ = 'u';
    var ir_ = 'o';
    var iV_ = 't';
    var jc_ = '%';
    var jl_ = '8';
    var jQ_ = 'C';
    var jS_ = 'y';
    var jv_ = 'f';
    var jy_ = '4';
    var kC_ = 'i';
    var KL_ = 'i';
    var Kq_ = 'A';
    var KR_ = '1';
    var kv_ = 'U';
    var ky_ = '%';
    var Ky_ = '8';
    var le_ = '5';
    var LE_ = 'I';
    var lK_ = 'B';
    var lL_ = 'A';
    var Lm_ = ';';
    var Lq_ = 'l';
    var lr_ = '%';
    var Lr_ = '8';
    var Ls_ = '%';
    var mH_ = 'a';
    var Mk_ = 'd';
    var mo_ = 'a';
    var Mq_ = '4';
    var mR_ = 'p';
    var Mx_ = '%';
    var mX_ = 'g';
    var mx_ = 't';
    var nj_ = 'E';
    var NK_ = '7';
    var nu_ = 'e';
    var nV_ = 'n';
    var nX_ = 'e';
    var Ny_ = 'C';
    var oC_ = ';';
    var oc_ = 'h';
    var od_ = 'E';
    var Oe_ = 'e';
    var OL_ = 'd';
    var OP_ = '1';
    var or_ = 'w';
    var OS_ = 'a';
    var oT_ = 'C';
    var ov_ = 'e';
    var OX_ = 'c';
    var Pb_ = '%';
    var Pd_ = ';';
    var pd_ = 'n';
    var pE_ = 'e';
    var pl_ = '%';
    var pq_ = '%';
    var PQ_ = 't';
    var Pr_ = 'm';
    var PT_ = 'A';
    var Pw_ = 'C';
    var Qe_ = 'E';
    var qk_ = '5';
    var ql_ = 'V';
    var QN_ = '9';
    var Qr_ = '%';
    var qX_ = 'E';
    var rD_ = '%';
    var rd_ = 'A';
    var Rl_ = 'd';
    var RN_ = 'e';
    var Ro_ = 'n';
    var ro_ = 't';
    var rs_ = 'o';
    var Rx_ = 'E';
    var Sb_ = 'e';
    var sE_ = 't';
    var Sg_ = 'D';
    var SJ_ = 'o';
    var ss_ = 'e';
    var St_ = 'o';
    var sz_ = '9';
    var tB_ = '0';
    var tc_ = 'g';
    var TG_ = ';';
    var tg_ = '8';
    var TP_ = 'e';
    var tQ_ = '6';
    var TR_ = 'e';
    var Ts_ = ';';
    var tW_ = 'B';
    var ua_ = 'd';
    var UD_ = 'r';
    var uE_ = 'E';
    var Uf_ = 'r';
    var UG_ = '8';
    var UM_ = '%';
    var up_ = 's';
    var UQ_ = 'o';
    var Uu_ = 'i';
    var uw_ = '%';
    var VB_ = '%';
    var vc_ = '%';
    var vE_ = 'E';
    var VH_ = '%';
    var VJ_ = 'e';
    var vK_ = 't';
    var vl_ = '9';
    var VS_ = '8';
    var Vv_ = ';';
    var vZ_ = '%';
    var WG_ = 'B';
    var wi_ = 'r';
    var wK_ = '%';
    var wO_ = '%';
    var Wq_ = 'A';
    var WU_ = 'B';
    var xE_ = 'B';
    var Xf_ = 's';
    var xh_ = '5';
    var XH_ = 'F';
    var xj_ = 'p';
    var XL_ = ';';
    var XM_ = '%';
    var xM_ = '5';
    var xq_ = 'i';
    var xV_ = 'f';
    var yb_ = 'B';
    var YB_ = 'e';
    var yg_ = ';';
    var YI_ = 'E';
    var YJ_ = 'E';
    var yk_ = '%';
    var Yk_ = 'u';
    var YL_ = 'e';
    var yM_ = 'F';
    var YM_ = 'n';
    var ym_ = 'y';
    var Yn_ = '4';
    var Yq_ = 'w';
    var YR_ = ';';
    var Ys_ = 'r';
    var yT_ = '0';
    var Yw_ = 'A';
    var Za_ = 'l';
    var ZC_ = '%';
    var ZG_ = '%';
    var zG_ = 'F';
    var zj_ = 'c';
    var zT_ = '%';
    var Zx_ = 'P';
    var zY_ = ';';
    var zz_ = '8';
    var xe_ = jE_('Zs_');
    var si_ = '_';
    var qe_ = '3';
    var GR_ = '_';
    var lJ_ = '9';
    var lb_ = '4';
    var Fx_ = '9';
    var vo_ = '3';
    var Wk_ = '0';
    var lP_ = '0';
    var aW_ = '7';
    var xt_ = '_';
    var GZ_ = '6';
    var Cj_ = '3';
    var Qv_ = '0';
    var gm_ = '6';
    var Pt_ = '2';
    var RF_ = '4';
    var Ji_ = '8';
})(document);
