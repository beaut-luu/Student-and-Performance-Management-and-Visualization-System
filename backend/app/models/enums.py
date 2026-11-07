from enum import Enum


class Jurisdiction(Enum):
    admin = 'admin'
    user = 'user'
    student = 'student'
    org = 'org'


class OrganizationRole(Enum):
    owner = 'owner'
    manager = 'manager'
    member = 'member'


class GroupRole(Enum):
    owner = 'owner'
    admin = 'admin'
    member = 'member'


class ActivityStatus(Enum):
    draft = 'draft'  # 草稿
    pending_review = 'pending_review'  # 待审核
    reject = 'reject'  # 已驳回
    published = 'published'  # 公示期
    cancelled = 'cancelled'  # 已取消
    finished = 'finished'  # 已完成


class ActivityRegistrationStatus(Enum):
    approved = 'approved'  # 被录用
    cancelled = 'cancelled'  # 已取消
    rejected = 'rejected'  # 被驳回
    check_in = 'check_in'  # 已签到
    pending = 'pending'  # 待审核


class GroupJoinMode(Enum):
    public = 'public'  # 自由加入
    approval = 'approval'  # 需审核
    private = 'private'  # 邀请制


class GroupStatus(Enum):
    normal = 'normal'  # 正常
    muted = 'muted'  # 全员禁言
    dissolved = 'dissolved'  # 已解散


class ChatMessageType(Enum):
    text = 'text'  # 文本
    image = 'image'  # 图片
    file = 'file'  # 文件
    system = 'system'  # 系统消息
    recalled = 'recalled'  # 已撤回


class ChatMessageStatus(Enum):
    normal = 'normal'  # 正常
    recalled = 'recalled'  # 已撤回


class MsgTypeStatus(Enum):
    all = 'all'  # 全体成员
    manager = 'manager'  # 仅管理员
