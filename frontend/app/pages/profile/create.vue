<template>
    <UPageSection class="max-w-2xl mx-auto">
        <template #header>
            <div class="space-y-1 mb-2! text-center">
                <h1 class="text-5xl font-semibold">Create Profile</h1>
                <p class="text-black">Fill out the form below to create your profile</p>
            </div>
        </template>
        <UPageCard variant="subtle" class="p-4 shadow-md bg-white outline outline-black">
            <UForm class="flex flex-col gap-3" :validate="validate" :state="state" @submit="submit">
                <h2 class="text-lg font-semibold">Personal Info</h2>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <UFormField label="Name" name="name" required>
                        <UInput placeholder="John" v-model="state.name" />
                    </UFormField>

                    <UFormField label="Age" name="age" required>
                        <UInputNumber :increment="false" :decrement="false" placeholder="18" v-model="state.age" />
                    </UFormField>
                </div>

                <UFormField label="Date of birth" name="dob" required>
                    <UInputDate v-model="state.dob" class="w-full" />
                </UFormField>

                <USeparator />

                <h2 class="text-lg font-semibold">Identity Information</h2>

                <UFormField label="Gender" name="gender" required>
                    <div class="w-full">
                        <USelect v-if="state.gender !== 'Other'" :items="genders" class="w-full" placeholder="Select"
                            v-model="state.gender" />

                        <UFieldGroup v-else class="flex gap-2 w-full">
                            <USelect :items="genders" class="w-1/2" v-model="state.gender" />
                            <UInput placeholder="Gender" class="w-1/2" v-model="state.gender_specified" />
                        </UFieldGroup>
                    </div>
                </UFormField>

                <UFormField label="Sexuality" name="sexuality" required>
                    <USelect :items="sexualities" class="w-full" placeholder="Select" v-model="state.sexuality" />
                </UFormField>

                <UFormField label="Bio" name="bio" required>
                    <UTextarea class="w-full" placeholder="Hello I like to do.." minlength="200" v-model="state.bio"
                        autoresize />
                </UFormField>

                <UButton type="submit" class="self-middle text-center">Submit</UButton>
            </UForm>
        </UPageCard>

        <a href="/" class="mt-0! hover:text-gray-900">Back &larr;</a>
    </UPageSection>
</template>


<script setup>

const genders = [
    'Male',
    'Female',
    'non-binary',
    'Other'
]

const sexualities = [
    'Heterosexual',
    'Homosexual',
    'Bisexual',
    'Other'
]

const state = reactive({
    name: '',
    age: undefined,
    dob: undefined,
    gender: undefined,
    gender_specified: undefined,
    sexuality: undefined,
    bio: ''
})

async function validate(state) {
    const errors = []
    if (!state.name) {
        errors.push({ name: 'name', message: 'Name is required' })
    }
    if (!state.dob) {
        errors.push({ name: 'dob', message: 'Dob is required' })
    }
    if (!state.age) {
        errors.push({ name: 'age', message: 'Age is required' })
    }
    if (!state.gender) {
        errors.push({ name: 'gender', message: 'Gender is required' })
    }
    if (!state.sexuality) {
        errors.push({ name: 'sexuality', message: 'Sexuality is required' })
    }
    if (!state.bio) {
        errors.push({ name: 'bio', message: 'Bio is required' })
    }
    return errors
}

async function submit() {
    const payload = {
        name: state.name,
        age: state.age,
        gender: state.gender,
        sexuality: state.sexuality,
        bio: state.bio
    }
    const response = await fetch('http://localhost:8000/profile/create', {
        method: 'POST',
        headers: {
            'Authorization': 'test',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    const data = await response.json()
    console.log(data)
}



</script>