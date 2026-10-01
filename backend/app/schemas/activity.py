from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ConfigDict
from app.models.enums import ActivityStatus


class ActivityIn(BaseModel):
    org_id: int = Field(..., description="活动承包组织")
    title: str = Field(..., min_length=1, max_length=50, description="活动标题")
    summary: str = Field(..., min_length=1, max_length=50, description="活动概述")
    content: str = Field(..., min_length=1, max_length=400, description="活动内容详情")
    category: str = Field(..., min_length=1, max_length=10, description="活动分类")
    location: str = Field(..., min_length=1, max_length=50, description="活动地点")
    start_time: datetime = Field(..., description="活动开始时间")
    end_time: datetime = Field(..., description="活动结束时间")
    register_start: datetime = Field(..., description="活动报名开始时间")
    register_deadline: datetime = Field(..., description="活动报名结束时间")
    capacity: int | None = Field(..., description="报名名额")
    need_approval: bool = Field(..., description="是否审核")
    fields: dict = Field(..., description="报名表格式")
    checkin: bool = Field(..., description="是否开启签到")

    @model_validator(mode="after")
    def checkin_time(self):
        if self.register_start <= datetime.now():
            raise ValueError("活动报名开始时间不能是过去的时间")
        if self.start_time <= self.register_start:
            raise ValueError("活动开始时间不能在活动报名开始时间之前")
        if self.end_time <= self.start_time:
            raise ValueError("活动开始时间不能在活动结束时间之后")
        if self.register_deadline <= self.end_time:
            raise ValueError("活动报名截止时间不能晚于活动结束时间")

        return self


class OrgOptionOut(BaseModel):
    """创建活动页的下拉框数据源：活动承包组织列表"""
    model_config = ConfigDict(from_attributes=True)
    org_id: int = Field(..., description="活动承包组织ID")
    name: str = Field(..., min_length=1, max_length=50, description="活动承包组织名称")


class ActivityCreatedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="活动ID")
    status: ActivityStatus = Field(..., description="活动状态")
