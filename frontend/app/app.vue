<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
import type { User } from './types/User';


const oauth2_url = {
  dev: "https://discord.com/oauth2/authorize?client_id=1442284848109846598&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauthorize&scope=identify+guilds.join+email",
  prod: ""
}.dev

provide("oauth2_url", oauth2_url)

const user_object = ref<User>({
  id: null,
  username: null,
  global_name: null,
  avatar: null,
  web_token: null
})

provide('user_object', user_object)

</script>

<style>
body {
    background-color: var(--color-bg-alt);
    font-family: 'Raleway', sans-serif;
    background-image:
        radial-gradient(#A45D5D 1px, transparent 1px),
        radial-gradient(#A45D5D 1px, #ffffff 1px);
    background-size: 20px 20px;
    background-position: 0 0, 20px 20px;
}
</style>