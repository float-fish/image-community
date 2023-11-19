CREATE DATABASE denoised_picture_community;

USE denoised_picture_community;

DROP TABLE IF EXISTS t_user;

DROP TABLE IF EXISTS t_head_picture;

DROP TABLE IF EXISTS t_origin_picture;

DROP TABLE IF EXISTS t_denoised_picture;

DROP TABLE IF EXISTS t_community_picture;

DROP TABLE IF EXISTS t_comment;

DROP TABLE IF EXISTS t_suspension_record;

DROP TABLE IF EXISTS t_admin;

DROP TABLE IF EXISTS t_web_information;

DROP TABLE IF EXISTS t_pending_picture;




/*==============================================================*/
/* Table: t_user_account                                         */
/*==============================================================*/

CREATE TABLE t_user
(
   user_id   INT AUTO_INCREMENT NOT NULL COMMENT"用户账号",
   head_picture_id   INT NOT NULL COMMENT"头像图片ID",
   email             VARCHAR(32) NOT NULL COMMENT"用户电子邮箱",
   user_password     VARCHAR(32) NOT NULL COMMENT"用户密码",
   user_name         VARCHAR(15) NOT NULL COMMENT"用户名",
   sex               CHAR(1) COMMENT"性别",
   telephone         VARCHAR(32) COMMENT"电话号码",
   register_time     DATETIME NOT NULL COMMENT"注册时间",
   PRIMARY KEY(user_id),
   UNIQUE(email)
);

alter table t_user comment'用户表';

/*==============================================================*/
/* Table: t_head_picture                                           */
/*==============================================================*/

CREATE TABLE t_head_picture
(
   head_picture_id    INT AUTO_INCREMENT NOT NULL COMMENT"头像ID",
   head_picture_path  VARCHAR(255) NOT NULL COMMENT"头像图片路径",
   PRIMARY KEY(head_picture_id)
);

alter table t_head_picture comment'头像表';

/*==============================================================*/
/* Table: t_origin_picture                                           */
/*==============================================================*/

CREATE TABLE t_origin_picture
(
   picture_id        INT AUTO_INCREMENT NOT NULL COMMENT '原始图片ID',
   picture_path      VARCHAR(255) NOT NULL COMMENT '图片路径',
   update_time       DATETIME NOT NULL COMMENT '上传时间',
   picture_name      VARCHAR(15) NOT NULL COMMENT '图片名字',
   collective_tag    BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否收藏',
   picture_owner_id  INT NOT NULL COMMENT'图片归属用户ID',
   PRIMARY KEY(picture_id)
);

ALTER TABLE t_origin_picture COMMENT '原始图片表';

/*==============================================================*/
/* Table: t_denoised_picture                                           */
/*==============================================================*/

CREATE TABLE t_denoised_picture
(
   picture_id        INT AUTO_INCREMENT NOT NULL COMMENT"去噪图片ID",
   picture_path      VARCHAR(255) NOT NULL COMMENT"图片路径",
   generating_time   DATETIME NOT NULL COMMENT"上传时间",
   picture_name      VARCHAR(15) NOT NULL COMMENT"图片名字",
   collective_tag    BOOLEAN NOT NULL DEFAULT FALSE COMMENT"是否收藏",
   denoising_mode    VARCHAR(20) NOT NULL COMMENT"去噪模式",
   picture_accuracy  DOUBLE NOT NULL COMMENT"准确度",
   picture_clarity   DOUBLE NOT NULL COMMENT"清晰度",
   origin_picture_id INT NOT NULL COMMENT"原始图片ID",
   PRIMARY KEY(picture_id)
);

alter table t_denoised_picture comment'去噪图片表';

/*==============================================================*/
/* Table: t_comunity_picture                                           */
/*==============================================================*/

CREATE TABLE t_community_picture
(
   picture_id        INT AUTO_INCREMENT NOT NULL COMMENT"社区图像ID",
   picture_path      VARCHAR(255) NOT NULL COMMENT"图片路径",
   upload_time       DATETIME NOT NULL COMMENT"上传时间",
   picture_name      VARCHAR(15) NOT NULL COMMENT"图片名字",
   picture_favor     INT DEFAULT 0 COMMENT"图片获赞数",
   picture_description VARCHAR(255) COMMENT"图片描述",
   picture_tag       VARCHAR(10)  COMMENT"图片标签",
   upload_user_id    INT COMMENT"上传用户ID",
   PRIMARY KEY(picture_id)
);

alter table t_community_picture comment'社区图片表';

/*==============================================================*/
/* Table: t_comment                                           */
/*==============================================================*/

CREATE TABLE t_comment
(
   comment_id        INT AUTO_INCREMENT NOT NULL COMMENT"评论记录ID",
   comment_text      VARCHAR(255) NOT NULL COMMENT"评论文字",
   linked_picture_id INT NOT NULL COMMENT"关联社区图像ID",
   PRIMARY KEY(comment_id)
);

alter table t_comment comment'评论记录表';

/*==============================================================*/
/* Table: t_suspension_record                                           */
/*==============================================================*/

CREATE TABLE t_suspension_record
(
   record_id        INT AUTO_INCREMENT NOT NULL COMMENT"评论记录ID",
   start_time       DATETIME NOT NULL COMMENT"封禁开始时间",
   end_time         DATETIME NOT NULL COMMENT"封禁结束时间",
   suspension_user_id INT NOT NULL COMMENT"封禁用户ID",
   PRIMARY KEY(record_id)
);

alter table t_suspension_record comment'评论记录表';

/*==============================================================*/
/* Table: t_admin                                           */
/*==============================================================*/

CREATE TABLE t_admin
(
   admin_account     VARCHAR(40) NOT NULL COMMENT"管理员账号",
   admin_password    VARCHAR(32) NOT NULL COMMENT"管理员密码",
   admin_name        VARCHAR(15) NOT NULL COMMENT"管理员姓名",
   PRIMARY KEY(admin_account)
);

alter table t_admin comment'管理员表';

/*==============================================================*/
/* Table: t_web_information                                           */
/*==============================================================*/

CREATE TABLE t_web_information
(
   web_date          DATE NOT NULL COMMENT"当前日期",
   user_daily_num    INT NOT NULL COMMENT"当日登录用户",
   new_image         INT NOT NULL COMMENT"新增图片",
   PRIMARY KEY(web_date)
);

alter table t_web_information  comment'网站信息表';

/*==============================================================*/
/* Table: t_pending_record                                         */
/*==============================================================*/

CREATE TABLE t_pending_record
(
   pending_id         INT AUTO_INCREMENT NOT NULL COMMENT"待审图片ID",
   picture_id         INT NOT NULL COMMENT"待审图片ID",
   picture_name       VARCHAR(15) NOT NULL COMMENT"图片名字",
   picture_description VARCHAR(255) NOT NULL COMMENT"图片描述",
   has_denoised       BOOLEAN NOT NULL COMMENT"是否去噪",
   PRIMARY KEY(pending_id)
);

alter table t_pending_record comment'待审图片表';



ALTER TABLE t_user ADD CONSTRAINT FK_user_head_picture
FOREIGN KEY (head_picture_id) REFERENCES t_head_picture(head_picture_id)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE t_origin_picture ADD CONSTRAINT FK_picture_owner
FOREIGN KEY (picture_owner_id) REFERENCES t_user(user_id)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE t_denoised_picture ADD CONSTRAINT FK_denoise_origin
FOREIGN KEY (origin_picture_id) REFERENCES t_origin_picture(picture_id)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE t_community_picture ADD CONSTRAINT FK_picture_uploader
FOREIGN KEY (upload_user_id) REFERENCES t_user(user_id)
ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE t_suspension_record ADD CONSTRAINT FK_account_suspension
FOREIGN KEY (suspension_user_id) REFERENCES t_user(user_id)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE t_comment ADD CONSTRAINT FK_pciture_comment
FOREIGN KEY (linked_picture_id) REFERENCES t_community_picture(picture_id)
ON DELETE CASCADE ON UPDATE CASCADE;


