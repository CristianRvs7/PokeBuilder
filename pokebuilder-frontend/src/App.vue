<script setup></script>

<template>
  <div class="scene">
    <div class="scene__cloud scene__cloud--a"></div>
    <div class="scene__cloud scene__cloud--b"></div>
    <div class="scene__cloud scene__cloud--c"></div>
    <svg class="scene__hills" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">
      <path
        class="hill hill--back"
        d="M0,140 C240,80 480,180 720,120 C960,60 1200,160 1440,110 L1440,220 L0,220 Z"
      />
      <path
        class="hill hill--front"
        d="M0,180 C200,140 500,200 760,150 C1040,100 1300,190 1440,150 L1440,220 L0,220 Z"
      />
    </svg>
    <router-view class="scene__content" />
  </div>
</template>

<style scoped>
.scene {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(
    180deg,
    var(--color-sky-top) 0%,
    var(--color-sky-bottom) 60%,
    var(--color-meadow-pale) 100%
  );
}

.scene__cloud {
  position: absolute;
  width: 120px;
  height: 46px;
  background: #ffffff;
  opacity: 0.85;
  border-radius: 999px;
  pointer-events: none;
}
.scene__cloud::before,
.scene__cloud::after {
  content: '';
  position: absolute;
  background: inherit;
  border-radius: 50%;
}
.scene__cloud::before {
  width: 60px;
  height: 60px;
  top: -28px;
  left: 14px;
}
.scene__cloud::after {
  width: 46px;
  height: 46px;
  top: -18px;
  left: 64px;
}

.scene__cloud--a {
  top: 10%;
  left: 6%;
  animation: drift 46s ease-in-out infinite alternate;
}
.scene__cloud--b {
  top: 20%;
  right: 8%;
  animation: drift 58s ease-in-out infinite alternate-reverse;
}
.scene__cloud--c {
  top: 7%;
  left: 48%;
  opacity: 0.65;
  animation: drift 34s ease-in-out infinite alternate;
}

@keyframes drift {
  from {
    transform: translateX(-18px);
  }
  to {
    transform: translateX(18px);
  }
}

.scene__hills {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 20vh;
  min-height: 130px;
  z-index: 1;
  pointer-events: none;
}
.hill--back {
  fill: var(--color-meadow-pale);
  opacity: 0.85;
}
.hill--front {
  fill: var(--color-meadow);
}

/* Clave del fix: sin esto, el contenido (sin position/z-index propios)
   se pinta ANTES que .scene__hills en el orden de apilamiento, y las
   colinas quedan encima tapando el texto. */
.scene__content {
  position: relative;
  z-index: 2;
}
</style>
