import{u as _,c as y,h as T,r as B,Q as J,W as qe,g as W,a8 as Re,X as ce,H as D,R as de,w as P,o as ke,A as Q,S as Qe,C as X,a9 as fe,a as De,K as ze,aa as Ve,a0 as we,a2 as Z,U as Oe,V as Ie}from"./index.aca000eb.js";import{h as O,b as Ke}from"./render.1220120f.js";import{c as ee,u as te,d as ve,e as Ne,a as je}from"./focus-manager.2fbb7ce5.js";import{u as Ue,c as Ge,v as Xe,g as U,d as Ee}from"./QBtn.0545539b.js";import{c as Ye,s as Je,g as Ze}from"./scroll.459c07c0.js";import{a as et}from"./dom.4211bfdb.js";var Dt=_({name:"QItemLabel",props:{overline:Boolean,caption:Boolean,header:Boolean,lines:[Number,String]},setup(e,{slots:t}){const n=y(()=>parseInt(e.lines,10)),l=y(()=>"q-item__label"+(e.overline===!0?" q-item__label--overline text-overline":"")+(e.caption===!0?" q-item__label--caption text-caption":"")+(e.header===!0?" q-item__label--header":"")+(n.value===1?" ellipsis":"")),o=y(()=>e.lines!==void 0&&n.value>1?{overflow:"hidden",display:"-webkit-box","-webkit-box-orient":"vertical","-webkit-line-clamp":n.value}:null);return()=>T("div",{style:o.value,class:l.value},O(t.default))}}),zt=_({name:"QItem",props:{...ee,...Ue,tag:{type:String,default:"div"},active:{type:Boolean,default:null},clickable:Boolean,dense:Boolean,insetLevel:Number,tabindex:[String,Number],focused:Boolean,manualFocus:Boolean},emits:["click","keyup"],setup(e,{slots:t,emit:n}){const{proxy:{$q:l}}=W(),o=te(e,l),{hasLink:c,linkAttrs:i,linkClass:u,linkTag:m,navigateOnClick:d}=Ge(),r=B(null),g=B(null),b=y(()=>e.clickable===!0||c.value===!0||e.tag==="label"),a=y(()=>e.disable!==!0&&b.value===!0),f=y(()=>"q-item q-item-type row no-wrap"+(e.dense===!0?" q-item--dense":"")+(o.value===!0?" q-item--dark":"")+(c.value===!0&&e.active===null?u.value:e.active===!0?` q-item--active${e.activeClass!==void 0?` ${e.activeClass}`:""}`:"")+(e.disable===!0?" disabled":"")+(a.value===!0?" q-item--clickable q-link cursor-pointer "+(e.manualFocus===!0?"q-manual-focusable":"q-focusable q-hoverable")+(e.focused===!0?" q-manual-focusable--focused":""):"")),w=y(()=>{if(e.insetLevel===void 0)return null;const s=l.lang.rtl===!0?"Right":"Left";return{["padding"+s]:16+e.insetLevel*56+"px"}});function k(s){a.value===!0&&(g.value!==null&&(s.qKeyEvent!==!0&&document.activeElement===r.value?g.value.focus():document.activeElement===g.value&&r.value.focus()),d(s))}function E(s){if(a.value===!0&&J(s,[13,32])===!0){qe(s),s.qKeyEvent=!0;const x=new MouseEvent("click",s);x.qKeyEvent=!0,r.value.dispatchEvent(x)}n("keyup",s)}function h(){const s=Ke(t.default,[]);return a.value===!0&&s.unshift(T("div",{class:"q-focus-helper",tabindex:-1,ref:g})),s}return()=>{const s={ref:r,class:f.value,style:w.value,role:"listitem",onClick:k,onKeyup:E};return a.value===!0?(s.tabindex=e.tabindex||"0",Object.assign(s,i.value)):b.value===!0&&(s["aria-disabled"]="true"),T(m.value,s,h())}}}),Vt=_({name:"QItemSection",props:{avatar:Boolean,thumbnail:Boolean,side:Boolean,top:Boolean,noWrap:Boolean},setup(e,{slots:t}){const n=y(()=>`q-item__section column q-item__section--${e.avatar===!0||e.side===!0||e.thumbnail===!0?"side":"main"}`+(e.top===!0?" q-item__section--top justify-start":" justify-center")+(e.avatar===!0?" q-item__section--avatar":"")+(e.thumbnail===!0?" q-item__section--thumbnail":"")+(e.noWrap===!0?" q-item__section--nowrap":""));return()=>T("div",{class:n.value},O(t.default))}}),Ot=_({name:"QList",props:{...ee,bordered:Boolean,dense:Boolean,separator:Boolean,padding:Boolean,tag:{type:String,default:"div"}},setup(e,{slots:t}){const n=W(),l=te(e,n.proxy.$q),o=y(()=>"q-list"+(e.bordered===!0?" q-list--bordered":"")+(e.dense===!0?" q-list--dense":"")+(e.separator===!0?" q-list--separator":"")+(l.value===!0?" q-list--dark":"")+(e.padding===!0?" q-list--padding":""));return()=>T(e.tag,{class:o.value},O(t.default))}});function tt(){if(window.getSelection!==void 0){const e=window.getSelection();e.empty!==void 0?e.empty():e.removeAllRanges!==void 0&&(e.removeAllRanges(),Re.is.mobile!==!0&&e.addRange(document.createRange()))}else document.selection!==void 0&&document.selection.empty()}const nt={target:{type:[Boolean,String,Element],default:!0},noParentEvent:Boolean},lt={...nt,contextMenu:Boolean};function ot({showing:e,avoidEmit:t,configureAnchorEl:n}){const{props:l,proxy:o,emit:c}=W(),i=B(null);let u=null;function m(a){return i.value===null?!1:a===void 0||a.touches===void 0||a.touches.length<=1}const d={};n===void 0&&(Object.assign(d,{hide(a){o.hide(a)},toggle(a){o.toggle(a),a.qAnchorHandled=!0},toggleKey(a){J(a,13)===!0&&d.toggle(a)},contextClick(a){o.hide(a),ce(a),D(()=>{o.show(a),a.qAnchorHandled=!0})},prevent:ce,mobileTouch(a){if(d.mobileCleanup(a),m(a)!==!0)return;o.hide(a),i.value.classList.add("non-selectable");const f=a.target;de(d,"anchor",[[f,"touchmove","mobileCleanup","passive"],[f,"touchend","mobileCleanup","passive"],[f,"touchcancel","mobileCleanup","passive"],[i.value,"contextmenu","prevent","notPassive"]]),u=setTimeout(()=>{u=null,o.show(a),a.qAnchorHandled=!0},300)},mobileCleanup(a){i.value.classList.remove("non-selectable"),u!==null&&(clearTimeout(u),u=null),e.value===!0&&a!==void 0&&tt()}}),n=function(a=l.contextMenu){if(l.noParentEvent===!0||i.value===null)return;let f;a===!0?o.$q.platform.is.mobile===!0?f=[[i.value,"touchstart","mobileTouch","passive"]]:f=[[i.value,"mousedown","hide","passive"],[i.value,"contextmenu","contextClick","notPassive"]]:f=[[i.value,"click","toggle","passive"],[i.value,"keyup","toggleKey","passive"]],de(d,"anchor",f)});function r(){Qe(d,"anchor")}function g(a){for(i.value=a;i.value.classList.contains("q-anchor--skip");)i.value=i.value.parentNode;n()}function b(){if(l.target===!1||l.target===""||o.$el.parentNode===null)i.value=null;else if(l.target===!0)g(o.$el.parentNode);else{let a=l.target;if(typeof l.target=="string")try{a=document.querySelector(l.target)}catch{a=void 0}a!=null?(i.value=a.$el||a,n()):(i.value=null,console.error(`Anchor: target "${l.target}" not found`))}}return P(()=>l.contextMenu,a=>{i.value!==null&&(r(),n(a))}),P(()=>l.target,()=>{i.value!==null&&r(),b()}),P(()=>l.noParentEvent,a=>{i.value!==null&&(a===!0?r():n())}),ke(()=>{b(),t!==!0&&l.modelValue===!0&&i.value===null&&c("update:modelValue",!1)}),Q(()=>{u!==null&&clearTimeout(u),r()}),{anchorEl:i,canShow:m,anchorEvents:d}}function it(e,t){const n=B(null);let l;function o(u,m){const d=`${m!==void 0?"add":"remove"}EventListener`,r=m!==void 0?m:l;u!==window&&u[d]("scroll",r,X.passive),window[d]("scroll",r,X.passive),l=m}function c(){n.value!==null&&(o(n.value),n.value=null)}const i=P(()=>e.noParentEvent,()=>{n.value!==null&&(c(),t())});return Q(i),{localScrollTarget:n,unconfigureScrollTarget:c,changeScrollEvent:o}}const at={modelValue:{type:Boolean,default:null},"onUpdate:modelValue":[Function,Array]},ut=["beforeShow","show","beforeHide","hide"];function rt({showing:e,canShow:t,hideOnRouteChange:n,handleShow:l,handleHide:o,processOnMount:c}){const i=W(),{props:u,emit:m,proxy:d}=i;let r;function g(h){e.value===!0?f(h):b(h)}function b(h){if(u.disable===!0||h!==void 0&&h.qAnchorHandled===!0||t!==void 0&&t(h)!==!0)return;const s=u["onUpdate:modelValue"]!==void 0;s===!0&&(m("update:modelValue",!0),r=h,D(()=>{r===h&&(r=void 0)})),(u.modelValue===null||s===!1)&&a(h)}function a(h){e.value!==!0&&(e.value=!0,m("beforeShow",h),l!==void 0?l(h):m("show",h))}function f(h){if(u.disable===!0)return;const s=u["onUpdate:modelValue"]!==void 0;s===!0&&(m("update:modelValue",!1),r=h,D(()=>{r===h&&(r=void 0)})),(u.modelValue===null||s===!1)&&w(h)}function w(h){e.value!==!1&&(e.value=!1,m("beforeHide",h),o!==void 0?o(h):m("hide",h))}function k(h){u.disable===!0&&h===!0?u["onUpdate:modelValue"]!==void 0&&m("update:modelValue",!1):h===!0!==e.value&&(h===!0?a:w)(r)}P(()=>u.modelValue,k),n!==void 0&&Xe(i)===!0&&P(()=>d.$route.fullPath,()=>{n.value===!0&&e.value===!0&&f()}),c===!0&&ke(()=>{k(u.modelValue)});const E={show:b,hide:f,toggle:g};return Object.assign(d,E),E}let st=1,ct=document.body;function dt(e,t){const n=document.createElement("div");if(n.id=t!==void 0?`q-portal--${t}--${st++}`:e,fe.globalNodes!==void 0){const l=fe.globalNodes.class;l!==void 0&&(n.className=l)}return ct.appendChild(n),n}function ft(e){e.remove()}const R=[];function vt(e,t){do{if(e.$options.name==="QMenu"){if(e.hide(t),e.$props.separateClosePopup===!0)return U(e)}else if(e.__qPortal===!0){const n=U(e);return n!==void 0&&n.$options.name==="QPopupProxy"?(e.hide(t),n):e}e=U(e)}while(e!=null)}const mt=_({name:"QPortal",setup(e,{slots:t}){return()=>t.default()}});function ht(e){for(e=e.parent;e!=null;){if(e.type.name==="QGlobalDialog")return!0;if(e.type.name==="QDialog"||e.type.name==="QMenu")return!1;e=e.parent}return!1}function gt(e,t,n,l){const o=B(!1),c=B(!1);let i=null;const u={},m=l==="dialog"&&ht(e);function d(g){if(g===!0){ve(u),c.value=!0;return}c.value=!1,o.value===!1&&(m===!1&&i===null&&(i=dt(!1,l)),o.value=!0,R.push(e.proxy),Ne(u))}function r(g){if(c.value=!1,g!==!0)return;ve(u),o.value=!1;const b=R.indexOf(e.proxy);b!==-1&&R.splice(b,1),i!==null&&(ft(i),i=null)}return De(()=>{r(!0)}),e.proxy.__qPortal=!0,ze(e.proxy,"contentEl",()=>t.value),{showPortal:d,hidePortal:r,portalIsActive:o,portalIsAccessible:c,renderPortal:()=>m===!0?n():o.value===!0?[T(Ve,{to:i},T(mt,n))]:void 0}}const bt={transitionShow:{type:String,default:"fade"},transitionHide:{type:String,default:"fade"},transitionDuration:{type:[String,Number],default:300}};function pt(e,t=()=>{},n=()=>{}){return{transitionProps:y(()=>{const l=`q-transition--${e.transitionShow||t()}`,o=`q-transition--${e.transitionHide||n()}`;return{appear:!0,enterFromClass:`${l}-enter-from`,enterActiveClass:`${l}-enter-active`,enterToClass:`${l}-enter-to`,leaveFromClass:`${o}-leave-from`,leaveActiveClass:`${o}-leave-active`,leaveToClass:`${o}-leave-to`}}),transitionStyle:y(()=>`--q-transition-duration: ${e.transitionDuration}ms`)}}function yt(){let e;const t=W();function n(){e=void 0}return we(n),Q(n),{removeTick:n,registerTick(l){e=l,D(()=>{e===l&&(Ee(t)===!1&&e(),e=void 0)})}}}function xt(){let e=null;const t=W();function n(){e!==null&&(clearTimeout(e),e=null)}return we(n),Q(n),{removeTimeout:n,registerTimeout(l,o){n(),Ee(t)===!1&&(e=setTimeout(()=>{e=null,l()},o))}}}const H=[];let A;function qt(e){A=e.keyCode===27}function kt(){A===!0&&(A=!1)}function wt(e){A===!0&&(A=!1,J(e,27)===!0&&H[H.length-1](e))}function Ce(e){window[e]("keydown",qt),window[e]("blur",kt),window[e]("keyup",wt),A=!1}function Et(e){Z.is.desktop===!0&&(H.push(e),H.length===1&&Ce("addEventListener"))}function me(e){const t=H.indexOf(e);t!==-1&&(H.splice(t,1),H.length===0&&Ce("removeEventListener"))}const L=[];function Te(e){L[L.length-1](e)}function Ct(e){Z.is.desktop===!0&&(L.push(e),L.length===1&&document.body.addEventListener("focusin",Te))}function Tt(e){const t=L.indexOf(e);t!==-1&&(L.splice(t,1),L.length===0&&document.body.removeEventListener("focusin",Te))}const{notPassiveCapture:z}=X,M=[];function V(e){const t=e.target;if(t===void 0||t.nodeType===8||t.classList.contains("no-pointer-events")===!0)return;let n=R.length-1;for(;n>=0;){const l=R[n].$;if(l.type.name==="QTooltip"){n--;continue}if(l.type.name!=="QDialog")break;if(l.props.seamless!==!0)return;n--}for(let l=M.length-1;l>=0;l--){const o=M[l];if((o.anchorEl.value===null||o.anchorEl.value.contains(t)===!1)&&(t===document.body||o.innerRef.value!==null&&o.innerRef.value.contains(t)===!1))e.qClickOutside=!0,o.onClickOutside(e);else return}}function St(e){M.push(e),M.length===1&&(document.addEventListener("mousedown",V,z),document.addEventListener("touchstart",V,z))}function he(e){const t=M.findIndex(n=>n===e);t!==-1&&(M.splice(t,1),M.length===0&&(document.removeEventListener("mousedown",V,z),document.removeEventListener("touchstart",V,z)))}let ge,be;function pe(e){const t=e.split(" ");return t.length!==2?!1:["top","center","bottom"].includes(t[0])!==!0?(console.error("Anchor/Self position must start with one of top/center/bottom"),!1):["left","middle","right","start","end"].includes(t[1])!==!0?(console.error("Anchor/Self position must end with one of left/middle/right/start/end"),!1):!0}function Pt(e){return e?!(e.length!==2||typeof e[0]!="number"||typeof e[1]!="number"):!0}const Y={"start#ltr":"left","start#rtl":"right","end#ltr":"right","end#rtl":"left"};["left","middle","right"].forEach(e=>{Y[`${e}#ltr`]=e,Y[`${e}#rtl`]=e});function ye(e,t){const n=e.split(" ");return{vertical:n[0],horizontal:Y[`${n[1]}#${t===!0?"rtl":"ltr"}`]}}function Bt(e,t){let{top:n,left:l,right:o,bottom:c,width:i,height:u}=e.getBoundingClientRect();return t!==void 0&&(n-=t[1],l-=t[0],c+=t[1],o+=t[0],i+=t[0],u+=t[1]),{top:n,bottom:c,height:u,left:l,right:o,width:i,middle:l+(o-l)/2,center:n+(c-n)/2}}function Ht(e,t,n){let{top:l,left:o}=e.getBoundingClientRect();return l+=t.top,o+=t.left,n!==void 0&&(l+=n[1],o+=n[0]),{top:l,bottom:l+1,height:1,left:o,right:o+1,width:1,middle:o,center:l}}function Lt(e,t){return{top:0,center:t/2,bottom:t,left:0,middle:e/2,right:e}}function xe(e,t,n,l){return{top:e[n.vertical]-t[l.vertical],left:e[n.horizontal]-t[l.horizontal]}}function Se(e,t=0){if(e.targetEl===null||e.anchorEl===null||t>5)return;if(e.targetEl.offsetHeight===0||e.targetEl.offsetWidth===0){setTimeout(()=>{Se(e,t+1)},10);return}const{targetEl:n,offset:l,anchorEl:o,anchorOrigin:c,selfOrigin:i,absoluteOffset:u,fit:m,cover:d,maxHeight:r,maxWidth:g}=e;if(Z.is.ios===!0&&window.visualViewport!==void 0){const $=document.body.style,{offsetLeft:q,offsetTop:C}=window.visualViewport;q!==ge&&($.setProperty("--q-pe-left",q+"px"),ge=q),C!==be&&($.setProperty("--q-pe-top",C+"px"),be=C)}const{scrollLeft:b,scrollTop:a}=n,f=u===void 0?Bt(o,d===!0?[0,0]:l):Ht(o,u,l);Object.assign(n.style,{top:0,left:0,minWidth:null,minHeight:null,maxWidth:g||"100vw",maxHeight:r||"100vh",visibility:"visible"});const{offsetWidth:w,offsetHeight:k}=n,{elWidth:E,elHeight:h}=m===!0||d===!0?{elWidth:Math.max(f.width,w),elHeight:d===!0?Math.max(f.height,k):k}:{elWidth:w,elHeight:k};let s={maxWidth:g,maxHeight:r};(m===!0||d===!0)&&(s.minWidth=f.width+"px",d===!0&&(s.minHeight=f.height+"px")),Object.assign(n.style,s);const x=Lt(E,h);let p=xe(f,x,c,i);if(u===void 0||l===void 0)G(p,f,x,c,i);else{const{top:$,left:q}=p;G(p,f,x,c,i);let C=!1;if(p.top!==$){C=!0;const S=2*l[1];f.center=f.top-=S,f.bottom-=S+2}if(p.left!==q){C=!0;const S=2*l[0];f.middle=f.left-=S,f.right-=S+2}C===!0&&(p=xe(f,x,c,i),G(p,f,x,c,i))}s={top:p.top+"px",left:p.left+"px"},p.maxHeight!==void 0&&(s.maxHeight=p.maxHeight+"px",f.height>p.maxHeight&&(s.minHeight=s.maxHeight)),p.maxWidth!==void 0&&(s.maxWidth=p.maxWidth+"px",f.width>p.maxWidth&&(s.minWidth=s.maxWidth)),Object.assign(n.style,s),n.scrollTop!==a&&(n.scrollTop=a),n.scrollLeft!==b&&(n.scrollLeft=b)}function G(e,t,n,l,o){const c=n.bottom,i=n.right,u=Ye(),m=window.innerHeight-u,d=document.body.clientWidth;if(e.top<0||e.top+c>m)if(o.vertical==="center")e.top=t[l.vertical]>m/2?Math.max(0,m-c):0,e.maxHeight=Math.min(c,m);else if(t[l.vertical]>m/2){const r=Math.min(m,l.vertical==="center"?t.center:l.vertical===o.vertical?t.bottom:t.top);e.maxHeight=Math.min(c,r),e.top=Math.max(0,r-c)}else e.top=Math.max(0,l.vertical==="center"?t.center:l.vertical===o.vertical?t.top:t.bottom),e.maxHeight=Math.min(c,m-e.top);if(e.left<0||e.left+i>d)if(e.maxWidth=Math.min(i,d),o.horizontal==="middle")e.left=t[l.horizontal]>d/2?Math.max(0,d-i):0;else if(t[l.horizontal]>d/2){const r=Math.min(d,l.horizontal==="middle"?t.middle:l.horizontal===o.horizontal?t.right:t.left);e.maxWidth=Math.min(i,r),e.left=Math.max(0,r-e.maxWidth)}else e.left=Math.max(0,l.horizontal==="middle"?t.middle:l.horizontal===o.horizontal?t.left:t.right),e.maxWidth=Math.min(i,d-e.left)}var It=_({name:"QMenu",inheritAttrs:!1,props:{...lt,...at,...ee,...bt,persistent:Boolean,autoClose:Boolean,separateClosePopup:Boolean,noRouteDismiss:Boolean,noRefocus:Boolean,noFocus:Boolean,fit:Boolean,cover:Boolean,square:Boolean,anchor:{type:String,validator:pe},self:{type:String,validator:pe},offset:{type:Array,validator:Pt},scrollTarget:Je,touchPosition:Boolean,maxHeight:{type:String,default:null},maxWidth:{type:String,default:null}},emits:[...ut,"click","escapeKey"],setup(e,{slots:t,emit:n,attrs:l}){let o=null,c,i,u;const m=W(),{proxy:d}=m,{$q:r}=d,g=B(null),b=B(!1),a=y(()=>e.persistent!==!0&&e.noRouteDismiss!==!0),f=te(e,r),{registerTick:w,removeTick:k}=yt(),{registerTimeout:E}=xt(),{transitionProps:h,transitionStyle:s}=pt(e),{localScrollTarget:x,changeScrollEvent:p,unconfigureScrollTarget:$}=it(e,re),{anchorEl:q,canShow:C}=ot({showing:b}),{hide:S}=rt({showing:b,canShow:C,handleShow:Me,handleHide:We,hideOnRouteChange:a,processOnMount:!0}),{showPortal:le,hidePortal:oe,renderPortal:Pe}=gt(m,g,Ae,"menu"),I={anchorEl:q,innerRef:g,onClickOutside(v){if(e.persistent!==!0&&b.value===!0)return S(v),(v.type==="touchstart"||v.target.classList.contains("q-dialog__backdrop"))&&qe(v),!0}},ie=y(()=>ye(e.anchor||(e.cover===!0?"center middle":"bottom start"),r.lang.rtl)),Be=y(()=>e.cover===!0?ie.value:ye(e.self||"top start",r.lang.rtl)),He=y(()=>(e.square===!0?" q-menu--square":"")+(f.value===!0?" q-menu--dark q-dark":"")),Le=y(()=>e.autoClose===!0?{onClick:$e}:{}),ae=y(()=>b.value===!0&&e.persistent!==!0);P(ae,v=>{v===!0?(Et(N),St(I)):(me(N),he(I))});function K(){je(()=>{let v=g.value;v&&v.contains(document.activeElement)!==!0&&(v=v.querySelector("[autofocus][tabindex], [data-autofocus][tabindex]")||v.querySelector("[autofocus] [tabindex], [data-autofocus] [tabindex]")||v.querySelector("[autofocus], [data-autofocus]")||v,v.focus({preventScroll:!0}))})}function Me(v){if(o=e.noRefocus===!1?document.activeElement:null,Ct(se),le(),re(),c=void 0,v!==void 0&&(e.touchPosition||e.contextMenu)){const j=Oe(v);if(j.left!==void 0){const{top:_e,left:Fe}=q.value.getBoundingClientRect();c={left:j.left-Fe,top:j.top-_e}}}i===void 0&&(i=P(()=>r.screen.width+"|"+r.screen.height+"|"+e.self+"|"+e.anchor+"|"+r.lang.rtl,F)),e.noFocus!==!0&&document.activeElement.blur(),w(()=>{F(),e.noFocus!==!0&&K()}),E(()=>{r.platform.is.ios===!0&&(u=e.autoClose,g.value.click()),F(),le(!0),n("show",v)},e.transitionDuration)}function We(v){k(),oe(),ue(!0),o!==null&&(v===void 0||v.qClickOutside!==!0)&&(((v&&v.type.indexOf("key")===0?o.closest('[tabindex]:not([tabindex^="-"])'):void 0)||o).focus(),o=null),E(()=>{oe(!0),n("hide",v)},e.transitionDuration)}function ue(v){c=void 0,i!==void 0&&(i(),i=void 0),(v===!0||b.value===!0)&&(Tt(se),$(),he(I),me(N)),v!==!0&&(o=null)}function re(){(q.value!==null||e.scrollTarget!==void 0)&&(x.value=Ze(q.value,e.scrollTarget),p(x.value,F))}function $e(v){u!==!0?(vt(d,v),n("click",v)):u=!1}function se(v){ae.value===!0&&e.noFocus!==!0&&et(g.value,v.target)!==!0&&K()}function N(v){n("escapeKey"),S(v)}function F(){Se({targetEl:g.value,offset:e.offset,anchorEl:q.value,anchorOrigin:ie.value,selfOrigin:Be.value,absoluteOffset:c,fit:e.fit,cover:e.cover,maxHeight:e.maxHeight,maxWidth:e.maxWidth})}function Ae(){return T(Ie,h.value,()=>b.value===!0?T("div",{role:"menu",...l,ref:g,tabindex:-1,class:["q-menu q-position-engine scroll"+He.value,l.class],style:[l.style,s.value],...Le.value},O(t.default)):null)}return Q(ue),Object.assign(d,{focus:K,updatePosition:F}),Pe}});const ne={left:!0,right:!0,up:!0,down:!0,horizontal:!0,vertical:!0},Mt=Object.keys(ne);ne.all=!0;function Kt(e){const t={};for(const n of Mt)e[n]===!0&&(t[n]=!0);return Object.keys(t).length===0?ne:(t.horizontal===!0?t.left=t.right=!0:t.left===!0&&t.right===!0&&(t.horizontal=!0),t.vertical===!0?t.up=t.down=!0:t.up===!0&&t.down===!0&&(t.vertical=!0),t.horizontal===!0&&t.vertical===!0&&(t.all=!0),t)}const Wt=["INPUT","TEXTAREA"];function Nt(e,t){return t.event===void 0&&e.target!==void 0&&e.target.draggable!==!0&&typeof t.handler=="function"&&Wt.includes(e.target.nodeName.toUpperCase())===!1&&(e.qClonedBy===void 0||e.qClonedBy.indexOf(t.uid)===-1)}export{Ot as Q,ut as a,xt as b,tt as c,rt as d,zt as e,Dt as f,Kt as g,Vt as h,bt as i,It as j,yt as k,pt as l,gt as m,me as n,Ct as o,Et as p,Tt as r,Nt as s,at as u};