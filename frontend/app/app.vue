<template>
  <NuxtPage />
</template>

<script setup lang="ts">

interface User {
  user_id: number,
  avatar: string,
  web_token: string
}


// should probably create an interface for this
const user_object = ref({
  user_id: null,
  avatar: null,
  web_token: null
})

provide("user_object", user_object)
  
</script>