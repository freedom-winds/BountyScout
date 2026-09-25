// src/types/alert_types.ts

export interface SlackMessage {
  text: string
  attachments: Array<{
    color: string
    title: string
    title_link: string
    text: string
    fields: Array<{
      title: string
      value: string
      short: boolean
    }>
    footer: string
  }>
}

export interface DiscordMessage {
  content: string
  embeds: any[]
}

export interface EmailDigest {
  subject: string
  body: string
}