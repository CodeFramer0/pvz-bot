<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Хедер -->
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>PVZ Dashboard</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <!-- Контейнер для страниц -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
