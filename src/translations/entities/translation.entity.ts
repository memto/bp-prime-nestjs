import { Column, Entity, PrimaryColumn } from 'typeorm';

@Entity()
export class Translation {
  @PrimaryColumn()
  id: number;

  @Column()
  text: string;

  @Column()
  audio_url: string;

  @Column()
  translate_id: number;

  @Column()
  translate_text: string;
}
