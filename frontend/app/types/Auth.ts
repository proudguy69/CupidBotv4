export interface Auth {
    success: boolean,
    profile: {
        user_id: number,
        avatar: string|null
    },
    web_token:string,
    message:string|null
}