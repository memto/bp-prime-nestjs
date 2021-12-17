import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { LoggerService } from 'src/logger/logger.service';
import { Translation } from './entities/translation.entity';
import { Repository } from 'typeorm';
import { validate } from 'class-validator';
import { CreateTranslationsReqDTO } from './dto/create-translation.req-dto';

@Injectable()
export class TranslationsService {
  constructor(
      private readonly logger: LoggerService = new Logger(TranslationsService.name),
      @InjectRepository(Translation) private readonly translationRepository: Repository<Translation>
    ) {}

  async GetListTranslations(paging) {
    const [result, total] = await this.translationRepository.findAndCount({
      take: paging.page_size, 
      skip: (paging.page_number - 1) * paging.page_size,
    });

    return {
      translations: result,
      pagination: {
        page_number: paging.page_number,
        page_size: paging.page_size,
        total_size: total,
      }
    }
  }

  async createTranslation(createTranslationReqDTO: CreateTranslationsReqDTO) {
    // Validation Flag
    let isOk = false;

    // Validate DTO against validate function from class-validator
    await validate(createTranslationReqDTO).then((errors) => {
      if (errors.length > 0) {
        this.logger.debug(`${errors}`);
      } else {
        isOk = true;
      }
    });

    if (isOk) {
      const translation = new Translation();

      // TODO: mapper
      translation.id = createTranslationReqDTO.id;
      translation.text = createTranslationReqDTO.text;
      translation.audio_url = createTranslationReqDTO.audio_url;
      translation.translate_id = createTranslationReqDTO.translate_id;
      translation.translate_text = createTranslationReqDTO.translate_text;

      return this.translationRepository.save(translation);
    }
  }
}
