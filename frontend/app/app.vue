<template>
  <UHeader>
    <template #title>
      Cupidv4
    </template>

    
    <template #right>
      <UNavigationMenu :items="items" />
      <UButton v-if="!user_object.username" variant="subtle" color="secondary" icon="logos:discord-icon">Login</UButton>
      <UButton
      v-if="user_object.username"
      variant="subtle"
      color="secondary"
      :avatar="{
        src: avatar_url
      }"
      >
      {{ user_object.username }}
    </UButton>
      <UColorModeButton/>
    </template>
  </UHeader>
  <NuxtPage />
</template>

<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import type { User } from '~/types/User'

const items:NavigationMenuItem[] = [

]

// should probably create an interface for this
const user_object = ref<User>({
  id: null,
  username: null,
  global_name: null,
  avatar: null,
  web_token: null
})
const avatar_url = ref('')

watch(user_object, (old:any, changed:any) => {
  avatar_url.value = `https://cdn.discordapp.com/avatars/${user_object.value.id}/${user_object.value.avatar}.png`
})



provide("user_object", user_object)
  
</script>