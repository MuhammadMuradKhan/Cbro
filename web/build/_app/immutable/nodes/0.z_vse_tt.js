import{_ as c}from"../chunks/preload-helper.0HuHagjb.js";import{r as u,g as n,i as _,$ as f,w as m}from"../chunks/runtime.-hGPaMd1.js";import{s as p,c as g,u as d,g as $,d as L}from"../chunks/scheduler.3IkOjBO1.js";import{S as y,i as S,d as v,t as b}from"../chunks/index.b4_itZyM.js";u("en-US",()=>c(()=>import("../chunks/en-US.JAQIzv30.js"),__vite__mapDeps([]),import.meta.url));u("zh-CN",()=>c(()=>import("../chunks/zh-CN.giVTFcLQ.js"),__vite__mapDeps([]),import.meta.url));const r="lang",h="en-US";let i=window.navigator.language;n()&&(i=n());localStorage.getItem(r)&&(i=localStorage.getItem(r));_({fallbackLocale:h,initialLocale:i,handleMissingMessage:o=>o.id.split(".").pop()});f.subscribe(o=>{localStorage.setItem(r,o)});const w=!0;async function I({url:o}){await m();let a="";return typeof process>"u"&&(a=o.searchParams.get("comfyUrl")||""),{comfyUrl:a}}const j=Object.freeze(Object.defineProperty({__proto__:null,load:I,prerender:w},Symbol.toStringTag,{value:"Module"}));function P(o){let a;const s=o[1].default,t=g(s,o,o[0],null);return{c(){t&&t.c()},l(e){t&&t.l(e)},m(e,l){t&&t.m(e,l),a=!0},p(e,[l]){t&&t.p&&(!a||l&1)&&d(t,s,e,e[0],a?L(s,e[0],l,null):$(e[0]),null)},i(e){a||(v(t,e),a=!0)},o(e){b(t,e),a=!1},d(e){t&&t.d(e)}}}function E(o,a,s){let{$$slots:t={},$$scope:e}=a;return o.$$set=l=>{"$$scope"in l&&s(0,e=l.$$scope)},[e,t]}class z extends y{constructor(a){super(),S(this,a,E,P,p,{})}}export{z as component,j as universal};
function __vite__mapDeps(indexes) {
  if (!__vite__mapDeps.viteFileDeps) {
    __vite__mapDeps.viteFileDeps = []
  }
  return indexes.map((i) => __vite__mapDeps.viteFileDeps[i])
}