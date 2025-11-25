<template>
    <UPageSection title="settings" description="For devs only!!">
        <UPageCard variant="subtle">
            <UForm>
                
                <!-- The purpose of this form is to emulate user settings after auth-->
                <UFormField label="User Id">
                    <UInput v-model="user_object.user_id" />
                </UFormField>

                <UFormField label="Profile Picture">
                    <UInput v-model="user_object.avatar" />
                </UFormField>

                <UFormField label="Web token">
                    <UInput v-model="user_object.web_token" />
                </UFormField>

                <UFieldGroup class="mt-2">
                    <UButton variant="soft" @click="simulateAuth">Simulate Auth</UButton>
                    <UButton>Submit</UButton>
                </UFieldGroup>

            </UForm>
        </UPageCard>
    </UPageSection>
</template>

<script setup lang="ts">
import type { Auth } from '~/types/Auth'
import type { User } from '~/types/User'

// this is a ref
const user_object = inject<Ref<User>>("user_object")!

async function simulateAuth() {
    const response = await fetch(`http://localhost:8000/authorize?code=fake`)
    const data:Auth = await response.json()
    user_object.value.user_id = data.profile.user_id
    user_object.value.avatar = data.profile.avatar
    user_object.value.web_token = data.web_token

    localStorage.setItem('web_token', data.web_token)
    localStorage.setItem('avatar', data.profile.avatar?data.profile.avatar:'')
}

</script>