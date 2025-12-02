<template>
  <UHeader>
    <template #title>
      Cupidv4
    </template>

    <UNavigationMenu :items="items" content-orientation="verticle" />
    <template #right>


      <UButton v-if="!user_object.username" variant="subtle" color="secondary" icon="logos:discord-icon"
        :to="oauth2_url">
        Login
      </UButton>

      <UButton v-if="user_object.username" variant="subtle" color="secondary" :avatar="{
        src: avatar_url
      }" to="/profile/settings">
        {{ user_object.username }}
      </UButton>
      <UColorModeButton />
    </template>
  </UHeader>
  <NuxtPage />
</template>

<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import type { User } from '~/types/User'
import type { Authorization } from '../types/Authorization'

const items: NavigationMenuItem[] = [
  {
    label: 'Profile',
    children: [
      {
        label: 'Create',
        to: '/profile/create'
      },
      {
        label: 'edit',
        to: '/profile/edit'
      }
    ]
  }
]

const oauth2_url = {
  dev: "https://discord.com/oauth2/authorize?client_id=1442284848109846598&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauthorize&scope=identify+guilds.join+email",
  prod: ""
}.dev


const avatar_url = ref('')
const user_object = inject<Ref<User>>('user_object')! 

watch(user_object, (old: any, changed: any) => {
  avatar_url.value = `https://cdn.discordapp.com/avatars/${user_object.value.id}/${user_object.value.avatar}.png`
})

onMounted(async () => {
  const web_token = localStorage.getItem('web_token')
  if (!web_token) { return }

  const username = localStorage.getItem('username')
  const user_id = localStorage.getItem('user_id')
  const avatar = localStorage.getItem('avatar')

  user_object.value.id = user_id
  user_object.value.username = username
  user_object.value.avatar = avatar

  avatar_url.value = `https://cdn.discordapp.com/avatars/${user_object.value.id}/${user_object.value.avatar}.png`

  if (username && user_id && avatar) {
    return
  }
  const response = await fetch(`http://localhost:8000/authorization?token=${web_token}`)
  const data: Authorization = await response.json()
  if (!data.success) {
    return
  }
  user_object.value = data.profile!
})


</script>
