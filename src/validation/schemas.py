from pydantic import BaseModel, Field
from typing import List

class Claim(BaseModel):
    text: str = Field(
        description="Cevaptaki iddia veya cümlenin metni."
    )
    numeric_value: str = Field(
        description="Eğer cümlede bir finansal sayı, tarih veya metrik varsa buraya yaz. Yoksa boş bırak."
    )
    source_quote: str = Field(
        description="Bu sayının veya bilginin alındığı kaynak metinden (PDF) birebir, kelimesi kelimesine alıntı."
    )

class SynthesizedResponse(BaseModel):
    claims: List[Claim] = Field(
        description="Cevaptaki tüm mantıksal parçaların/iddiaların listesi."
    )
    final_answer: str = Field(
        description="Kullanıcıya gösterilecek, akıcı bir dille yazılmış nihai cevap."
    )