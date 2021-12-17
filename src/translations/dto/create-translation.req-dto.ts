import { IsNotEmpty, IsNumber, IsString } from 'class-validator';

export class CreateTranslationsReqDTO {
  @IsNotEmpty()
  @IsNumber()
  id: number;

  @IsNotEmpty()
  @IsString()
  text?: string;

  @IsNotEmpty()
  @IsString()
  audio_url: string;

  @IsNotEmpty()
  @IsNumber()
  translate_id: number;

  @IsNotEmpty()
  @IsString()
  translate_text?: string;
}
