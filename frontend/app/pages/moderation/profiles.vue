<template>
  <Navbar />

  <div class="flex items-center justify-center min-h-screen px-6">
    <div class="grid grid-cols-1 lg:grid-cols-5 gap-10 w-full max-w-8xl mx-20">

      <div
        class="lg:col-span-2 rounded-2xl p-6 bg-white/90 dark:bg-zinc-900/90 backdrop-blur shadow-lg"
      >
        <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
          <UIcon name="i-heroicons-users" class="w-5 h-5" />
          Users
        </h2>

        <ul class="space-y-3 max-h-[75vh] overflow-y-auto">
          <li
            v-for="(user, id) in users"
            :key="id"
            @click="selectUser(id)"
            class="p-4 rounded-xl cursor-pointer transition flex items-center gap-3 bg-gray-100 hover:bg-gray-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 mx-2 my-3"
            :class="{ 'ring-2 ring-primary': selectedUserId === id }"
          >
            <UIcon name="i-heroicons-user" class="w-5 h-5" />
            {{ user.username }}
          </li>
        </ul>
      </div>

      <div
        class="lg:col-span-3 rounded-2xl p-8 bg-white/90 dark:bg-zinc-900/90 backdrop-blur shadow-lg"
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-semibold flex items-center gap-2">
            <UIcon name="i-heroicons-identification" class="w-6 h-6" />
            User Profile
          </h2>


          <UButton
            v-if="selectedUser"
            icon="i-heroicons-pencil-square"
            variant="ghost"
            @click="editing = !editing"
          />
        </div>


        <div v-if="selectedUser" class="space-y-6">
          <div class="flex gap-8 items-start">
            <img
              :src="selectedUser.avatarUrl || 'https://placehold.co/180x180'"
              class="w-44 h-44 rounded-full object-cover ring-4 ring-gray-200 dark:ring-zinc-700"
            />

            <div v-if="!editing" class="space-y-3 flex-1">
              <p class="text-3xl font-semibold flex items-center gap-2">
                <UIcon name="i-heroicons-user-circle" />
                {{ selectedUser.username }}
              </p>

              <p class="flex items-center gap-2">
                <UIcon name="i-heroicons-hashtag" />
                UID: {{ selectedUserId }}
              </p>

              <p class="flex items-center gap-2">
                <UIcon name="i-heroicons-identification" />
                Displayname : {{ selectedUser.name }}
              </p>

              <p class="flex items-center gap-2">
                <UIcon name="i-heroicons-clock" />
                Age : {{ selectedUser.age }} years old
              </p>

              <p class="flex items-center gap-2">
                <UIcon name="i-heroicons-calendar-days" />
                Birthday : {{ selectedUser.dob }}
              </p>

              <p class="flex items-center gap-2">
                <UIcon name="i-heroicons-face-smile" />
                Gender : {{ selectedUser.gender }}
              </p>

              <p
                v-if="selectedUser.gender === 'Other'"
                class="flex items-center gap-2"
              >
                <UIcon name="i-heroicons-pencil" />
                Specified gender : {{ selectedUser.gender_specified }}
              </p>

              <p class="flex items-center gap-2">
                <UIcon name="i-heroicons-heart" />
                Sexuality : {{ selectedUser.sexuality }}
              </p>
            </div>



            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-3 flex-1">
              <UInput v-model="form.name" placeholder="Name" />
              <UInput v-model.number="form.age" type="number" placeholder="Age" />
              <UInput v-model="form.dob" placeholder="Date of birth" />
              <UInput v-model="form.gender" placeholder="Gender" />
              <UInput
                v-if="form.gender === 'Other'"
                v-model="form.gender_specified"
                placeholder="Specify Gender"
              />
              <UInput v-model="form.sexuality" placeholder="Sexuality" />
            </div>
          </div>

          <div v-if="!editing" class="flex items-start gap-3 border rounded-xl min-h-[140px] p-4">
            <UIcon name="i-heroicons-document-text" class="mt-1" />
            <p class="text-gray-700 dark:text-gray-300">
              {{ selectedUser.bio }}
            </p>
          </div>

          <div v-else>
            <UTextarea v-model="form.bio" placeholder="Bio" />
          </div>

          <div class="flex justify-end gap-4 pt-4">
            <UButton
              icon="i-heroicons-x-mark"
              @click="reject"
            >
              Reject
            </UButton>
            

            <UButton
              icon="i-heroicons-check"
              @click="accept"
            >
              Accept
            </UButton>
          </div>
        </div>

        <p v-else class="text-gray-500 italic">
          Select a user to see details.
        </p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
type User = {
  username: string
  avatarUrl: string
  name: string
  age: number
  dob: string
  gender: string
  gender_specified?: string
  sexuality: string
  bio: string
}

const users: Record<string, User> = {
  "123": {
    username: "JohnDoe",
    avatarUrl: "https://i.pinimg.com/736x/f8/92/77/f892775164c9394a32932ad6dfe52935.jpg",
    name: "John",
    age: 24,
    dob: "2000-01-01",
    gender: "Male",
    sexuality: "Heterosexual",
    bio: "Default ahh person"
  },
  "135": {
    username: "JaneDoe",
    avatarUrl: "https://i.pinimg.com/736x/f8/92/77/f892775164c9394a32932ad6dfe52935.jpg",
    name: "Jane",
    age: 22,
    dob: "2002-03-12",
    gender: "Female",
    sexuality: "Bisexual",
    bio: "Female ver of jhon"
  },
  "246": {
    username: "Obama",
    avatarUrl: "https://i.pinimg.com/736x/f8/92/77/f892775164c9394a32932ad6dfe52935.jpg",
    name: "Obama",
    age: 26,
    dob: "1998-07-08",
    gender: "Other",
    gender_specified: "Agender",
    sexuality: "Other",
    bio: "Balls"
  },
  "789": {
    username: "Bob",
    avatarUrl: "https://i.pinimg.com/736x/f8/92/77/f892775164c9394a32932ad6dfe52935.jpg",
    name: "Bob",
    age: 28,
    dob: "1996-11-21",
    gender: "Male",
    sexuality: "Homosexual",
    bio: "Gay bob"
  }
}

const selectedUserId = ref<string | null>(null)
const editing = ref(false)

const selectedUser = computed(() =>
  selectedUserId.value ? users[selectedUserId.value] : null
)

const form = reactive<User>({
  username: '',
  avatarUrl: '',
  name: '',
  age: 0,
  dob: '',
  gender: '',
  sexuality: '',
  bio: ''
})

function selectUser(id: string) {
  selectedUserId.value = id
  editing.value = false
  Object.assign(form, users[id])
}

function accept() {
  if (!selectedUserId.value) return
  users[selectedUserId.value] = { ...form }
}

function reject() {
  selectedUserId.value = null
  editing.value = false
}

async function sendData(){
  /// could send data here
}
</script>
