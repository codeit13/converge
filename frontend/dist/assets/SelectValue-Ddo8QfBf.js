import{ao as Le,y as I,E as M,h as E,j as F,ah as Ce,M as z,ap as Q,aq as _e,f as B,o as _,w as g,d as $,u as e,a6 as L,A as Z,k as x,ar as Ve,l as ue,p as de,v as He,z as ce,B as J,as as Fe,a as pe,q as O,H as Ke,am as G,at as We,au as ze,av as je,aw as Ue,L as fe,G as oe,ax as Ye,ay as Ge,g as Xe,az as Je,aA as we,i as Se,T as ae,aB as Ze,aC as Qe,J as xe,aD as et,aE as Be,N as Te,e as me,F as tt,t as ot,c as Pe,P as Y,n as at,b as nt}from"./index-C6yP06Ol.js";import{C as Ie}from"./chevron-down-D2zeU1nN.js";import{i as j,O as lt,C as N,v as ie,p as st,S as rt}from"./Textarea-k2BuJuhI.js";function it(r){const a=Le({nonce:I()});return M(()=>{var t;return(r==null?void 0:r.value)||((t=a.nonce)==null?void 0:t.value)})}function be(r,a=Number.NEGATIVE_INFINITY,t=Number.POSITIVE_INFINITY){return Math.min(t,Math.max(a,r))}const ut=E({__name:"SelectTrigger",props:{disabled:{type:Boolean},reference:{},asChild:{type:Boolean},as:{default:"button"}},setup(r){const a=r,t=j(),{forwardRef:c,currentElement:o}=F(),l=M(()=>{var f;return((f=t.disabled)==null?void 0:f.value)||a.disabled});t.contentId||(t.contentId=Ce(void 0,"reka-select-content")),z(()=>{t.onTriggerChange(o.value)});const{getItems:i}=Q(),{search:s,handleTypeaheadSearch:u,resetTypeahead:n}=_e();function v(){l.value||(t.onOpenChange(!0),n())}function p(f){v(),t.triggerPointerDownPosRef.value={x:Math.round(f.pageX),y:Math.round(f.pageY)}}return(f,y)=>(_(),B(e(Ve),{"as-child":"",reference:f.reference},{default:g(()=>{var k,q,D,R;return[$(e(L),{ref:e(c),role:"combobox",type:f.as==="button"?"button":void 0,"aria-controls":e(t).contentId,"aria-expanded":e(t).open.value||!1,"aria-required":(k=e(t).required)==null?void 0:k.value,"aria-autocomplete":"none",disabled:l.value,dir:(q=e(t))==null?void 0:q.dir.value,"data-state":(D=e(t))!=null&&D.open.value?"open":"closed","data-disabled":l.value?"":void 0,"data-placeholder":(R=e(t).modelValue)!=null&&R.value?void 0:"","as-child":f.asChild,as:f.as,onClick:y[0]||(y[0]=h=>{var b;(b=h==null?void 0:h.currentTarget)==null||b.focus()}),onPointerdown:y[1]||(y[1]=h=>{if(h.pointerType==="touch")return h.preventDefault();const b=h.target;b.hasPointerCapture(h.pointerId)&&b.releasePointerCapture(h.pointerId),h.button===0&&h.ctrlKey===!1&&(p(h),h.preventDefault())}),onPointerup:y[2]||(y[2]=Z(h=>{h.pointerType==="touch"&&p(h)},["prevent"])),onKeydown:y[3]||(y[3]=h=>{const b=e(s)!=="";!(h.ctrlKey||h.altKey||h.metaKey)&&h.key.length===1&&b&&h.key===" "||(e(u)(h.key,e(i)()),e(lt).includes(h.key)&&(v(),h.preventDefault()))})},{default:g(()=>[x(f.$slots,"default")]),_:3},8,["type","aria-controls","aria-expanded","aria-required","disabled","dir","data-state","data-disabled","data-placeholder","as-child","as"])]}),_:3},8,["reference"]))}}),dt=E({__name:"SelectPortal",props:{to:{},disabled:{type:Boolean},defer:{type:Boolean},forceMount:{type:Boolean}},setup(r){const a=r;return(t,c)=>(_(),B(e(He),ue(de(a)),{default:g(()=>[x(t.$slots,"default")]),_:3},16))}}),[ve,ct]=ce("SelectItemAlignedPosition"),pt=E({inheritAttrs:!1,__name:"SelectItemAlignedPosition",props:{asChild:{type:Boolean},as:{}},emits:["placed"],setup(r,{emit:a}){const t=r,c=a,{getItems:o}=Q(),l=j(),i=U(),s=I(!1),u=I(!0),n=I(),{forwardRef:v,currentElement:p}=F(),{viewport:f,selectedItem:y,selectedItemText:k,focusSelectedItem:q}=i;function D(){if(l.triggerElement.value&&l.valueElement.value&&n.value&&p.value&&(f!=null&&f.value)&&(y!=null&&y.value)&&(k!=null&&k.value)){const b=l.triggerElement.value.getBoundingClientRect(),d=p.value.getBoundingClientRect(),C=l.valueElement.value.getBoundingClientRect(),m=k.value.getBoundingClientRect();if(l.dir.value!=="rtl"){const V=m.left-d.left,H=C.left-V,K=b.left-H,W=b.width+K,le=Math.max(W,d.width),se=window.innerWidth-N,re=be(H,N,Math.max(N,se-le));n.value.style.minWidth=`${W}px`,n.value.style.left=`${re}px`}else{const V=d.right-m.right,H=window.innerWidth-C.right-V,K=window.innerWidth-b.right-H,W=b.width+K,le=Math.max(W,d.width),se=window.innerWidth-N,re=be(H,N,Math.max(N,se-le));n.value.style.minWidth=`${W}px`,n.value.style.right=`${re}px`}const w=o().map(V=>V.ref),S=window.innerHeight-N*2,T=f.value.scrollHeight,P=window.getComputedStyle(p.value),A=Number.parseInt(P.borderTopWidth,10),X=Number.parseInt(P.paddingTop,10),he=Number.parseInt(P.borderBottomWidth,10),qe=Number.parseInt(P.paddingBottom,10),ge=A+X+T+qe+he,De=Math.min(y.value.offsetHeight*5,ge),ye=window.getComputedStyle(f.value),Me=Number.parseInt(ye.paddingTop,10),Oe=Number.parseInt(ye.paddingBottom,10),ee=b.top+b.height/2-N,Re=S-ee,ne=y.value.offsetHeight/2,Ae=y.value.offsetTop+ne,te=A+X+Ae,Ne=ge-te;if(te<=ee){const V=y.value===w[w.length-1];n.value.style.bottom="0px";const H=p.value.clientHeight-f.value.offsetTop-f.value.offsetHeight,K=Math.max(Re,ne+(V?Oe:0)+H+he),W=te+K;n.value.style.height=`${W}px`}else{const V=y.value===w[0];n.value.style.top="0px";const K=Math.max(ee,A+f.value.offsetTop+(V?Me:0)+ne)+Ne;n.value.style.height=`${K}px`,f.value.scrollTop=te-ee+f.value.offsetTop}n.value.style.margin=`${N}px 0`,n.value.style.minHeight=`${De}px`,n.value.style.maxHeight=`${S}px`,c("placed"),requestAnimationFrame(()=>s.value=!0)}}const R=I("");z(async()=>{await J(),D(),p.value&&(R.value=window.getComputedStyle(p.value).zIndex)});function h(b){b&&u.value===!0&&(D(),q==null||q(),u.value=!1)}return Fe(l.triggerElement,()=>{D()}),ct({contentWrapper:n,shouldExpandOnScrollRef:s,onScrollButtonChange:h}),(b,d)=>(_(),pe("div",{ref_key:"contentWrapperElement",ref:n,style:Ke({display:"flex",flexDirection:"column",position:"fixed",zIndex:R.value})},[$(e(L),O({ref:e(v),style:{boxSizing:"border-box",maxHeight:"100%"}},{...b.$attrs,...t}),{default:g(()=>[x(b.$slots,"default")]),_:3},16)],4))}}),ft=E({__name:"SelectPopperPosition",props:{side:{},sideOffset:{},align:{default:"start"},alignOffset:{},avoidCollisions:{type:Boolean},collisionBoundary:{},collisionPadding:{default:N},arrowPadding:{},sticky:{},hideWhenDetached:{type:Boolean},positionStrategy:{},updatePositionStrategy:{},disableUpdateOnLayoutShift:{type:Boolean},prioritizePosition:{type:Boolean},reference:{},asChild:{type:Boolean},as:{}},setup(r){const t=G(r);return(c,o)=>(_(),B(e(We),O(e(t),{style:{boxSizing:"border-box","--reka-select-content-transform-origin":"var(--reka-popper-transform-origin)","--reka-select-content-available-width":"var(--reka-popper-available-width)","--reka-select-content-available-height":"var(--reka-popper-available-height)","--reka-select-trigger-width":"var(--reka-popper-anchor-width)","--reka-select-trigger-height":"var(--reka-popper-anchor-height)"}}),{default:g(()=>[x(c.$slots,"default")]),_:3},16))}}),mt={onViewportChange:()=>{},itemTextRefCallback:()=>{},itemRefCallback:()=>{}},[U,$e]=ce("SelectContent"),vt=E({__name:"SelectContentImpl",props:{position:{default:"item-aligned"},bodyLock:{type:Boolean,default:!0},side:{},sideOffset:{},align:{default:"start"},alignOffset:{},avoidCollisions:{type:Boolean},collisionBoundary:{},collisionPadding:{},arrowPadding:{},sticky:{},hideWhenDetached:{type:Boolean},positionStrategy:{},updatePositionStrategy:{},disableUpdateOnLayoutShift:{type:Boolean},prioritizePosition:{type:Boolean},reference:{},asChild:{type:Boolean},as:{}},emits:["closeAutoFocus","escapeKeyDown","pointerDownOutside"],setup(r,{emit:a}){const t=r,c=a,o=j();ze(),je(t.bodyLock);const{CollectionSlot:l,getItems:i}=Q(),s=I();Ue(s);const{search:u,handleTypeaheadSearch:n}=_e(),v=I(),p=I(),f=I(),y=I(!1),k=I(!1),q=I(!1);function D(){p.value&&s.value&&we([p.value,s.value])}fe(y,()=>{D()});const{onOpenChange:R,triggerPointerDownPosRef:h}=o;oe(m=>{if(!s.value)return;let w={x:0,y:0};const S=P=>{var A,X;w={x:Math.abs(Math.round(P.pageX)-(((A=h.value)==null?void 0:A.x)??0)),y:Math.abs(Math.round(P.pageY)-(((X=h.value)==null?void 0:X.y)??0))}},T=P=>{var A;P.pointerType!=="touch"&&(w.x<=10&&w.y<=10?P.preventDefault():(A=s.value)!=null&&A.contains(P.target)||R(!1),document.removeEventListener("pointermove",S),h.value=null)};h.value!==null&&(document.addEventListener("pointermove",S),document.addEventListener("pointerup",T,{capture:!0,once:!0})),m(()=>{document.removeEventListener("pointermove",S),document.removeEventListener("pointerup",T,{capture:!0})})});function b(m){const w=m.ctrlKey||m.altKey||m.metaKey;if(m.key==="Tab"&&m.preventDefault(),!w&&m.key.length===1&&n(m.key,i()),["ArrowUp","ArrowDown","Home","End"].includes(m.key)){let T=[...i().map(P=>P.ref)];if(["ArrowUp","End"].includes(m.key)&&(T=T.slice().reverse()),["ArrowUp","ArrowDown"].includes(m.key)){const P=m.target,A=T.indexOf(P);T=T.slice(A+1)}setTimeout(()=>we(T)),m.preventDefault()}}const d=M(()=>t.position==="popper"?t:{}),C=G(d.value);return $e({content:s,viewport:v,onViewportChange:m=>{v.value=m},itemRefCallback:(m,w,S)=>{const T=!k.value&&!S,P=ie(o.modelValue.value,w,o.by);if(o.multiple.value){if(q.value)return;(P||T)&&(p.value=m,P&&(q.value=!0))}else(P||T)&&(p.value=m);T&&(k.value=!0)},selectedItem:p,selectedItemText:f,onItemLeave:()=>{var m;(m=s.value)==null||m.focus()},itemTextRefCallback:(m,w,S)=>{const T=!k.value&&!S;(ie(o.modelValue.value,w,o.by)||T)&&(f.value=m)},focusSelectedItem:D,position:t.position,isPositioned:y,searchRef:u}),(m,w)=>(_(),B(e(l),null,{default:g(()=>[$(e(Ye),{"as-child":"",onMountAutoFocus:w[6]||(w[6]=Z(()=>{},["prevent"])),onUnmountAutoFocus:w[7]||(w[7]=S=>{var T;c("closeAutoFocus",S),!S.defaultPrevented&&((T=e(o).triggerElement.value)==null||T.focus({preventScroll:!0}),S.preventDefault())})},{default:g(()=>[$(e(Ge),{"as-child":"","disable-outside-pointer-events":"",onFocusOutside:w[2]||(w[2]=Z(()=>{},["prevent"])),onDismiss:w[3]||(w[3]=S=>e(o).onOpenChange(!1)),onEscapeKeyDown:w[4]||(w[4]=S=>c("escapeKeyDown",S)),onPointerDownOutside:w[5]||(w[5]=S=>c("pointerDownOutside",S))},{default:g(()=>[(_(),B(Xe(m.position==="popper"?ft:pt),O({...m.$attrs,...e(C)},{id:e(o).contentId,ref:S=>{s.value=e(Je)(S)},role:"listbox","data-state":e(o).open.value?"open":"closed",dir:e(o).dir.value,style:{display:"flex",flexDirection:"column",outline:"none"},onContextmenu:w[0]||(w[0]=Z(()=>{},["prevent"])),onPlaced:w[1]||(w[1]=S=>y.value=!0),onKeydown:b}),{default:g(()=>[x(m.$slots,"default")]),_:3},16,["id","data-state","dir","onKeydown"]))]),_:3})]),_:3})]),_:3}))}}),ht=E({inheritAttrs:!1,__name:"SelectProvider",props:{context:{}},setup(r){return st(r.context),$e(mt),(t,c)=>x(t.$slots,"default")}}),gt={key:1},yt=E({inheritAttrs:!1,__name:"SelectContent",props:{forceMount:{type:Boolean},position:{},bodyLock:{type:Boolean},side:{},sideOffset:{},align:{},alignOffset:{},avoidCollisions:{type:Boolean},collisionBoundary:{},collisionPadding:{},arrowPadding:{},sticky:{},hideWhenDetached:{type:Boolean},positionStrategy:{},updatePositionStrategy:{},disableUpdateOnLayoutShift:{type:Boolean},prioritizePosition:{type:Boolean},reference:{},asChild:{type:Boolean},as:{}},emits:["closeAutoFocus","escapeKeyDown","pointerDownOutside"],setup(r,{emit:a}){const t=r,o=Se(t,a),l=j(),i=I();z(()=>{i.value=new DocumentFragment});const s=I(),u=M(()=>t.forceMount||l.open.value);return(n,v)=>{var p;return u.value?(_(),B(e(Ze),{key:0,ref_key:"presenceRef",ref:s,present:!0},{default:g(()=>[$(vt,ue(de({...e(o),...n.$attrs})),{default:g(()=>[x(n.$slots,"default")]),_:3},16)]),_:3},512)):!((p=s.value)!=null&&p.present)&&i.value?(_(),pe("div",gt,[(_(),B(Qe,{to:i.value},[$(ht,{context:e(l)},{default:g(()=>[x(n.$slots,"default")]),_:3},8,["context"])],8,["to"]))])):ae("",!0)}}}),[ke,wt]=ce("SelectItem"),bt=E({__name:"SelectItem",props:{value:{},disabled:{type:Boolean},textValue:{},asChild:{type:Boolean},as:{}},emits:["select"],setup(r,{emit:a}){const t=r,c=a,{disabled:o}=xe(t),l=j(),i=U(),{forwardRef:s,currentElement:u}=F(),{CollectionItem:n}=Q(),v=M(()=>{var d;return ie((d=l.modelValue)==null?void 0:d.value,t.value,l.by)}),p=I(!1),f=I(t.textValue??""),y=Ce(void 0,"reka-select-item-text"),k="select.select";async function q(d){if(d.defaultPrevented)return;const C={originalEvent:d,value:t.value};et(k,D,C)}async function D(d){await J(),c("select",d),!d.defaultPrevented&&(o.value||(l.onValueChange(t.value),l.multiple.value||l.onOpenChange(!1)))}async function R(d){var C;await J(),!d.defaultPrevented&&(o.value?(C=i.onItemLeave)==null||C.call(i):d.currentTarget.focus({preventScroll:!0}))}async function h(d){var C;await J(),!d.defaultPrevented&&d.currentTarget===Be()&&((C=i.onItemLeave)==null||C.call(i))}async function b(d){var m;await J(),!(d.defaultPrevented||((m=i.searchRef)==null?void 0:m.value)!==""&&d.key===" ")&&(rt.includes(d.key)&&q(d),d.key===" "&&d.preventDefault())}if(t.value==="")throw new Error("A <SelectItem /> must have a value prop that is not an empty string. This is because the Select value can be set to an empty string to clear the selection and show the placeholder.");return z(()=>{u.value&&i.itemRefCallback(u.value,t.value,t.disabled)}),wt({value:t.value,disabled:o,textId:y,isSelected:v,onItemTextChange:d=>{f.value=((f.value||(d==null?void 0:d.textContent))??"").trim()}}),(d,C)=>(_(),B(e(n),{value:{textValue:f.value}},{default:g(()=>[$(e(L),{ref:e(s),role:"option","aria-labelledby":e(y),"data-highlighted":p.value?"":void 0,"aria-selected":v.value,"data-state":v.value?"checked":"unchecked","aria-disabled":e(o)||void 0,"data-disabled":e(o)?"":void 0,tabindex:e(o)?void 0:-1,as:d.as,"as-child":d.asChild,onFocus:C[0]||(C[0]=m=>p.value=!0),onBlur:C[1]||(C[1]=m=>p.value=!1),onPointerup:q,onPointerdown:C[2]||(C[2]=m=>{m.currentTarget.focus({preventScroll:!0})}),onTouchend:C[3]||(C[3]=Z(()=>{},["prevent","stop"])),onPointermove:R,onPointerleave:h,onKeydown:b},{default:g(()=>[x(d.$slots,"default")]),_:3},8,["aria-labelledby","data-highlighted","aria-selected","data-state","aria-disabled","data-disabled","tabindex","as","as-child"])]),_:3},8,["value"]))}}),Ct=E({__name:"SelectItemIndicator",props:{asChild:{type:Boolean},as:{default:"span"}},setup(r){const a=r,t=ke();return(c,o)=>e(t).isSelected.value?(_(),B(e(L),O({key:0,"aria-hidden":"true"},a),{default:g(()=>[x(c.$slots,"default")]),_:3},16)):ae("",!0)}}),_t=E({inheritAttrs:!1,__name:"SelectItemText",props:{asChild:{type:Boolean},as:{default:"span"}},setup(r){const a=r,t=j(),c=U(),o=ke(),{forwardRef:l,currentElement:i}=F(),s=M(()=>{var u,n;return{value:o.value,disabled:o.disabled.value,textContent:((u=i.value)==null?void 0:u.textContent)??((n=o.value)==null?void 0:n.toString())??""}});return z(()=>{i.value&&(o.onItemTextChange(i.value),c.itemTextRefCallback(i.value,o.value,o.disabled.value),t.onOptionAdd(s.value))}),Te(()=>{t.onOptionRemove(s.value)}),(u,n)=>(_(),B(e(L),O({id:e(o).textId,ref:e(l)},{...a,...u.$attrs}),{default:g(()=>[x(u.$slots,"default")]),_:3},16,["id"]))}}),St=E({__name:"SelectViewport",props:{nonce:{},asChild:{type:Boolean},as:{}},setup(r){const a=r,{nonce:t}=xe(a),c=it(t),o=U(),l=o.position==="item-aligned"?ve():void 0,{forwardRef:i,currentElement:s}=F();z(()=>{o==null||o.onViewportChange(s.value)});const u=I(0);function n(v){const p=v.currentTarget,{shouldExpandOnScrollRef:f,contentWrapper:y}=l??{};if(f!=null&&f.value&&(y!=null&&y.value)){const k=Math.abs(u.value-p.scrollTop);if(k>0){const q=window.innerHeight-N*2,D=Number.parseFloat(y.value.style.minHeight),R=Number.parseFloat(y.value.style.height),h=Math.max(D,R);if(h<q){const b=h+k,d=Math.min(q,b),C=b-d;y.value.style.height=`${d}px`,y.value.style.bottom==="0px"&&(p.scrollTop=C>0?C:0,y.value.style.justifyContent="flex-end")}}}u.value=p.scrollTop}return(v,p)=>(_(),pe(tt,null,[$(e(L),O({ref:e(i),"data-reka-select-viewport":"",role:"presentation"},{...v.$attrs,...a},{style:{position:"relative",flex:1,overflow:"hidden auto"},onScroll:n}),{default:g(()=>[x(v.$slots,"default")]),_:3},16),$(e(L),{as:"style",nonce:e(c)},{default:g(()=>p[0]||(p[0]=[me(" /* Hide scrollbars cross-browser and enable momentum scroll for touch devices */ [data-reka-select-viewport] { scrollbar-width:none; -ms-overflow-style: none; -webkit-overflow-scrolling: touch; } [data-reka-select-viewport]::-webkit-scrollbar { display: none; } ")])),_:1},8,["nonce"])],64))}}),Ee=E({__name:"SelectScrollButtonImpl",emits:["autoScroll"],setup(r,{emit:a}){const t=a,{getItems:c}=Q(),o=U(),l=I(null);function i(){l.value!==null&&(window.clearInterval(l.value),l.value=null)}oe(()=>{const n=c().map(v=>v.ref).find(v=>v===Be());n==null||n.scrollIntoView({block:"nearest"})});function s(){l.value===null&&(l.value=window.setInterval(()=>{t("autoScroll")},50))}function u(){var n;(n=o.onItemLeave)==null||n.call(o),l.value===null&&(l.value=window.setInterval(()=>{t("autoScroll")},50))}return Te(()=>i()),(n,v)=>{var p;return _(),B(e(L),O({"aria-hidden":"true",style:{flexShrink:0}},(p=n.$parent)==null?void 0:p.$props,{onPointerdown:s,onPointermove:u,onPointerleave:v[0]||(v[0]=()=>{i()})}),{default:g(()=>[x(n.$slots,"default")]),_:3},16)}}}),xt=E({__name:"SelectScrollUpButton",props:{asChild:{type:Boolean},as:{}},setup(r){const a=U(),t=a.position==="item-aligned"?ve():void 0,{forwardRef:c,currentElement:o}=F(),l=I(!1);return oe(i=>{var s,u;if((s=a.viewport)!=null&&s.value&&((u=a.isPositioned)!=null&&u.value)){let n=function(){l.value=v.scrollTop>0};const v=a.viewport.value;n(),v.addEventListener("scroll",n),i(()=>v.removeEventListener("scroll",n))}}),fe(o,()=>{o.value&&(t==null||t.onScrollButtonChange(o.value))}),(i,s)=>l.value?(_(),B(Ee,{key:0,ref:e(c),onAutoScroll:s[0]||(s[0]=()=>{const{viewport:u,selectedItem:n}=e(a);u!=null&&u.value&&(n!=null&&n.value)&&(u.value.scrollTop=u.value.scrollTop-n.value.offsetHeight)})},{default:g(()=>[x(i.$slots,"default")]),_:3},512)):ae("",!0)}}),Bt=E({__name:"SelectScrollDownButton",props:{asChild:{type:Boolean},as:{}},setup(r){const a=U(),t=a.position==="item-aligned"?ve():void 0,{forwardRef:c,currentElement:o}=F(),l=I(!1);return oe(i=>{var s,u;if((s=a.viewport)!=null&&s.value&&((u=a.isPositioned)!=null&&u.value)){let n=function(){const p=v.scrollHeight-v.clientHeight;l.value=Math.ceil(v.scrollTop)<p};const v=a.viewport.value;n(),v.addEventListener("scroll",n),i(()=>v.removeEventListener("scroll",n))}}),fe(o,()=>{o.value&&(t==null||t.onScrollButtonChange(o.value))}),(i,s)=>l.value?(_(),B(Ee,{key:0,ref:e(c),onAutoScroll:s[0]||(s[0]=()=>{const{viewport:u,selectedItem:n}=e(a);u!=null&&u.value&&(n!=null&&n.value)&&(u.value.scrollTop=u.value.scrollTop+n.value.offsetHeight)})},{default:g(()=>[x(i.$slots,"default")]),_:3},512)):ae("",!0)}}),Tt=E({__name:"SelectValue",props:{placeholder:{default:""},asChild:{type:Boolean},as:{default:"span"}},setup(r){const a=r,{forwardRef:t,currentElement:c}=F(),o=j();z(()=>{o.valueElement=c});const l=M(()=>{var v;let s=[];const u=Array.from(o.optionsSet.value),n=p=>u.find(f=>f.value===p);return Array.isArray(o.modelValue.value)?s=o.modelValue.value.map(p=>{var f;return((f=n(p))==null?void 0:f.textContent)??""}):s=[((v=n(o.modelValue.value))==null?void 0:v.textContent)??""],s.filter(Boolean)}),i=M(()=>l.value.length?l.value.join(", "):a.placeholder);return(s,u)=>(_(),B(e(L),{ref:e(t),as:s.as,"as-child":s.asChild,style:{pointerEvents:"none"},"data-placeholder":l.value.length?void 0:a.placeholder},{default:g(()=>[x(s.$slots,"default",{selectedLabel:l.value,modelValue:e(o).modelValue.value},()=>[me(ot(i.value),1)])]),_:3},8,["as","as-child","data-placeholder"]))}}),Pt=E({__name:"SelectIcon",props:{asChild:{type:Boolean},as:{default:"span"}},setup(r){return(a,t)=>(_(),B(e(L),{"aria-hidden":"true",as:a.as,"as-child":a.asChild},{default:g(()=>[x(a.$slots,"default",{},()=>[t[0]||(t[0]=me("▼"))])]),_:3},8,["as","as-child"]))}});/**
 * @license lucide-vue-next v0.477.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const It=Pe("CheckIcon",[["path",{d:"M20 6 9 17l-5-5",key:"1gmf2c"}]]);/**
 * @license lucide-vue-next v0.477.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const $t=Pe("ChevronUpIcon",[["path",{d:"m18 15-6-6-6 6",key:"153udz"}]]),At=Object.assign({inheritAttrs:!1},{__name:"SelectContent",props:{forceMount:{type:Boolean,required:!1},position:{type:String,required:!1,default:"popper"},bodyLock:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},class:{type:null,required:!1}},emits:["closeAutoFocus","escapeKeyDown","pointerDownOutside"],setup(r,{emit:a}){const t=r,c=a,o=M(()=>{const{class:i,...s}=t;return s}),l=Se(o,c);return(i,s)=>(_(),B(e(dt),null,{default:g(()=>[$(e(yt),O({...e(l),...i.$attrs},{class:e(Y)("relative z-50 max-h-96 min-w-32 overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",r.position==="popper"&&"data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1",t.class)}),{default:g(()=>[$(e(qt)),$(e(St),{class:at(e(Y)("p-1",r.position==="popper"&&"h-[--reka-select-trigger-height] w-full min-w-[--reka-select-trigger-width]"))},{default:g(()=>[x(i.$slots,"default")]),_:3},8,["class"]),$(e(Et))]),_:3},16,["class"])]),_:3}))}}),kt={class:"absolute right-2 flex h-3.5 w-3.5 items-center justify-center"},Nt={__name:"SelectItem",props:{value:{type:null,required:!0},disabled:{type:Boolean,required:!1},textValue:{type:String,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},class:{type:null,required:!1}},setup(r){const a=r,t=M(()=>{const{class:o,...l}=a;return l}),c=G(t);return(o,l)=>(_(),B(e(bt),O(e(c),{class:e(Y)("relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",a.class)}),{default:g(()=>[nt("span",kt,[$(e(Ct),null,{default:g(()=>[$(e(It),{class:"h-4 w-4"})]),_:1})]),$(e(_t),null,{default:g(()=>[x(o.$slots,"default")]),_:3})]),_:3},16,["class"]))}},Et={__name:"SelectScrollDownButton",props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1},class:{type:null,required:!1}},setup(r){const a=r,t=M(()=>{const{class:o,...l}=a;return l}),c=G(t);return(o,l)=>(_(),B(e(Bt),O(e(c),{class:e(Y)("flex cursor-default items-center justify-center py-1",a.class)}),{default:g(()=>[x(o.$slots,"default",{},()=>[$(e(Ie))])]),_:3},16,["class"]))}},qt={__name:"SelectScrollUpButton",props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1},class:{type:null,required:!1}},setup(r){const a=r,t=M(()=>{const{class:o,...l}=a;return l}),c=G(t);return(o,l)=>(_(),B(e(xt),O(e(c),{class:e(Y)("flex cursor-default items-center justify-center py-1",a.class)}),{default:g(()=>[x(o.$slots,"default",{},()=>[$(e($t))])]),_:3},16,["class"]))}},Lt={__name:"SelectTrigger",props:{disabled:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},class:{type:null,required:!1}},setup(r){const a=r,t=M(()=>{const{class:o,...l}=a;return l}),c=G(t);return(o,l)=>(_(),B(e(ut),O(e(c),{class:e(Y)("flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background data-[placeholder]:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50 [&>span]:truncate text-start",a.class)}),{default:g(()=>[x(o.$slots,"default"),$(e(Pt),{"as-child":""},{default:g(()=>[$(e(Ie),{class:"w-4 h-4 opacity-50 shrink-0"})]),_:1})]),_:3},16,["class"]))}},Vt={__name:"SelectValue",props:{placeholder:{type:String,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(r){const a=r;return(t,c)=>(_(),B(e(Tt),ue(de(a)),{default:g(()=>[x(t.$slots,"default")]),_:3},16))}};export{Lt as _,Vt as a,At as b,Nt as c};
