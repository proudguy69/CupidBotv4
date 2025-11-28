<template>
    <UButton disabled @click="send">Send Request</UButton>
    <br>
    code: {{ code }}
    <br>
    response: {{ result }}
    <br>
    <a :href="oauth2_url">oauth</a>
</template>

<script setup lang=ts>
import type { User } from '~/types/User'
import type { Auth } from '~/types/Auth'

const oauth2_url = "https://discord.com/oauth2/authorize?client_id=1442284848109846598&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauthorize&scope=identify+guilds.join+email"

const code:Ref = ref("")
const result = ref({})
const route = useRoute()
const router = useRouter()
const user_object = inject<Ref<User>>('user_object')!


async function send() {
    const response = await fetch(`http://localhost:8000/authorize?code=${code.value}`)
    const data:Auth = await response.json()
    user_object.value = data.profile
    console.log(user_object.value.avatar)
}

onMounted(async () => {
    code.value = route.query.code
    if (!code) {
        router.push('/')
        return
    }
    const response = await fetch(`http://localhost:8000/authorize?code=${code.value}`)
    const data:Auth = await response.json()
    if (!data.success) {
        console.log(data)
        router.push('/')
        return
    }
    user_object.value = data.profile
    localStorage.setItem('web_token', data.web_token)
    localStorage.setItem('username', data.profile.username!)
    localStorage.setItem('user_id', data.profile.id!)
    localStorage.setItem('avatar', data.profile.avatar!)
    router.push('/')
})

</script>