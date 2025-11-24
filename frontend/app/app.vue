<template>
  <NuxtPage />
</template>

<script setup>


// should probably create an interface for this
const user_object = ref({
  user_id: null,
  avatar: null,
  web_token: null
})

provide("user_object", user_object)
  
</script>