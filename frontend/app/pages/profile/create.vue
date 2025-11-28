<template>
    <UPageSection
    title="Profile Create"
    >
        <UPageCard
        variant="subtle"
        >
            <UForm
            class="flex flex-col gap-2"
            :validate="validate"
            :state="state"
            @submit="submit"
            >

                <h2>Personal Info</h2>

                <UFormField label="Name" name="name" required="">
                    <UInput
                    placeholder="John"
                    v-model="state.name"
                    />
                </UFormField>

                <UFormField label="Age" name="age" required="">
                    <UInputNumber
                    :increment="false"
                    :decrement="false"
                    placeholder="18"
                    v-model="state.age"
                    />
                </UFormField>

                <UFormField label="Date of birth" name="dob" required="">
                    <UInputDate
                    v-model="state.dob"
                    />
                </UFormField>

                <USeparator />

                <h2>Identity Information</h2>

                <UFormField label="Gender" name="gender" required="">
                    <USelect
                    :items="genders"
                    class="w-45"
                    v-model="state.gender"
                    v-if="state.gender != 'Other'"
                    placeholder="Select"
                    />
                    <UFieldGroup v-if="state.gender == 'Other'">
                        <USelect
                        :items="genders"
                        class="w-25"
                        v-model="state.gender"
                        />
                        <UInput
                        placeholder="Gender"
                        class="w-25"
                        v-model="state.gender_specified"
                        />
                    </UFieldGroup>
                </UFormField>

                <UFormField label="Sexuality" name="sexuality" required="">
                    <USelect
                    :items="sexualities"
                    class="w-45"
                    placeholder="Select"
                    v-model="state.sexuality"
                    />
                </UFormField>

                <UFormField label="Bio" name="bio" required="">
                    <UTextarea
                    class="w-full"
                    placeholder="Hello I like to do.."
                    minlength="200"
                    v-model="state.bio"
                    autoresize
                    />
                </UFormField>
                <UButton type="submit">Submit</UButton>
            </UForm>
        </UPageCard>
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
        errors.push({name: 'name', message: 'Name is required'})
    }
    if (!state.dob) {
        errors.push({name: 'dob', message: 'Dob is required'})
    }
    if (!state.age) {
        errors.push({name: 'age', message: 'Age is required'})
    }
    if (!state.gender) {
        errors.push({name: 'gender', message: 'Gender is required'})
    }
    if (!state.sexuality) {
        errors.push({name: 'sexuality', message: 'Sexuality is required'})
    }
    if (!state.bio) {
        errors.push({name: 'bio', message: 'Bio is required'})
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