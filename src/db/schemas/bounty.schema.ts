// src/db/schemas/bounty.schema.ts
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose'
import { Document, Types } from 'mongoose'

@Schema({ timestamps: true })
export class BountySchema extends Document {
  @Prop({ required: true, unique: true })
  id: string

  @Prop({ required: true })
  repository: string

  @Prop({ required: true })
  title: string

  @Prop({ required: true })
  description: string

  @Prop({ required: true, default: 0 })
  priorityScore: number

  @Prop({ required: false })
  rewardAmount: number | null

  @Prop({ required: true })
  lastUpdated: Date

  @Prop({ required: true })
  sourceScanId: string

  @Prop({ required: true, default: 'open' })
  status: 'open' | 'claimed' | 'expired'

  @Prop({ required: false })
  claimedAt: Date | null

  @Prop({ required: false, default: {} })
  metadata: Record<string, unknown>
}

export const BountyModel = SchemaFactory.createForClass(BountySchema)