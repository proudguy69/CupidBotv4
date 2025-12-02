import type { User } from "./User"

export interface Auth {
    success: boolean,
    profile: User,
    web_token:string,
    message:string|null
}