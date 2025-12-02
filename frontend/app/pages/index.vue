<style>
.font-raleway {
    font-family: "Raleway", sans-serif;
}
</style>

<template>
    <Navbar />

    <div class="background">
        <UPageHero class="bg-transparent" orientation="horizontal" reverse>

            <template #title>
                <h1 class="text-9xl font-raleway shadow-text">Hey, welcome!</h1>
            </template>

            <template #description>
                <p class="text-lg font-raleway text-gray-800">Let's get you started.</p>
            </template>
            
            <template #links>
                <UModal v-model:open="open">
                    <UButton
                    color="secondary"
                    icon="i-lucide-square-play"
                    variant="solid"
                    label="Get started"
                    v-if="user_object.id"
                    />


                    <template #header>
                        <h3 class="text-2xl font-semibold">Get started</h3>
                        <p class="text-gray-500">Ready to create your profile?</p>
                        <UButton icon="i-lucide-x" class="ml-auto" @click="close"/>
                    </template>

                    <template #body>
                        <div class="flex items-center justify-center gap-8 py-4">
                            <UButton color="secondary" variant="soft" to="/profile/create" class="px-6 py-3">
                                Create Profile
                            </UButton>

                            <div class="flex flex-col items-center gap-1">
                                <span class="text-xs text-gray-500 italic">or</span>
                                <div class="w-px h-10 bg-gray-300"></div>
                                <span class="text-xs text-gray-500">Action may require login</span>
                            </div>

                            <UButton color="secondary" variant="soft" to="/profile/edit" class="px-6 py-3">
                                Edit Profile
                            </UButton>
                        </div>
                    </template>
                </UModal>

                <UButton
                color="secondary"
                icon="logos:discord-icon"
                variant="solid"
                label="Login"
                :to="oauth2_url"
                v-if="!user_object.id"
                />


                <UButton color="neutral" variant="subtle" trailing-icon="i-lucide-arrow-right" to="/about">
                    Learn more
                </UButton>
            </template>

            <img src="https://i.pinimg.com/736x/f8/92/77/f892775164c9394a32932ad6dfe52935.jpg" alt="cupidv4"
                class="w-1/2 rounded-full ring ring-default mx-auto" />
        </UPageHero>
    </div>
</template>

<script setup lang="ts">
import type { User } from '~/types/User';


const open = ref(false)

function close() {
    open.value = !open.value
}

const oauth2_url = inject("oauth2_url")!

const user_object = inject<Ref<User>>("user_object")!


</script>
