import { Controller, Get, Post, Req, Res, Body } from '@nestjs/common';
import { TranslationsService } from './translations.service';
import { CreateTranslationsReqDTO } from './dto/create-translation.req-dto';

@Controller('translations')
export class TranslationsController {
  constructor(private readonly translationService: TranslationsService) {}

  @Get()
  findAll(@Req() req) {
    const page_number = !!req.query.page_number ? parseInt(req.query.page_number, 10) : 1;
    const page_size = !!req.query.page_size ? parseInt(req.query.page_size, 10) : 10;
    const paging = {
      page_number: page_number,
      page_size: page_size
    }
    return this.translationService.GetListTranslations(paging);
  }

  @Post()
  async createTranslation(@Req() req, @Res() res, @Body() body) {
    const createTranslationReqDTO = new CreateTranslationsReqDTO();

    createTranslationReqDTO.id = 1;
    createTranslationReqDTO.text = "text";
    createTranslationReqDTO.audio_url = "audio_url";
    createTranslationReqDTO.translate_id = 2;
    createTranslationReqDTO.translate_text = "translate_text";

    const ret = await this.translationService.createTranslation(createTranslationReqDTO);
    res.status(200).json(ret);
  }
}
