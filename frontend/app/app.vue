<template>
  <UHeader>
    <template #title>
      Cupidv4
    </template>

    
    <template #right>
      <UNavigationMenu :items="items" />
      <UButton variant="subtle" color="secondary" icon="logos:discord-icon">Login</UButton>
      <UColorModeButton/>
    </template>
  </UHeader>
  <NuxtPage />
</template>

<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const items:NavigationMenuItem[] = [

]

// should probably create an interface for this
const user_object = ref({
  user_id: null,
  avatar: null,
  web_token: null
})

provide("user_object", user_object)
  
</script>