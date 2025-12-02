import type { User } from "./User"

export interface Authorization {
    success: boolean,
    profile: User|null,
}