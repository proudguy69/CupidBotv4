<template>
    <UPageSection>
        <UCard variant="subtle">
            <UForm>
                <UButton @click="logout">Logout</UButton>
            </UForm>
        </UCard>
    </UPageSection>
</template>

<script setup lang="ts">
import type { User } from '~/types/User';

const user_object = inject<Ref<User>>('user_object')!

async function logout() {
    localStorage.clear()
    useRouter().push('/')
    

    user_object.value = {
        id: null,
        username: null,
        global_name: null,
        avatar: null,
        web_token: null
    }
}

</script>