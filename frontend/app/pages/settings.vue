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

// this is a ref
const user_object: any = inject("user_object")

async function simulateAuth() {
    const response = await fetch(`http://localhost:8000/authorize?code=fake`)
    const data = await response.json()
    console.log(data)
}

</script>