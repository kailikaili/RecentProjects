


CREATE TABLE sys_operation_dim (
	operation_code VARCHAR(6) NOT NULL, 
	operation_name VARCHAR(100) NOT NULL, 
	unit_level BOOLEAN DEFAULT 'f' NOT NULL,  -- 是否是集团级用户
	shop_level BOOLEAN DEFAULT 'f' NOT NULL,  -- 是否是商户级用户
	root_level BOOLEAN DEFAULT 'f' NOT NULL,  -- 是否是终端级用户
	operator_level BOOLEAN DEFAULT 'f' NOT NULL, 
	PRIMARY KEY (operation_code)
);


CREATE TABLE unit_info (
	unit_no VARCHAR(4) NOT NULL, 
	unit_name VARCHAR(100) NOT NULL, 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	weixin_token VARCHAR(255) DEFAULT '' NOT NULL, 
	remark TEXT DEFAULT '' NOT NULL, 
	PRIMARY KEY (unit_no)
);


CREATE TABLE sys_city_dim (
	id SERIAL NOT NULL, 
	city VARCHAR(255) NOT NULL, 
	level INTEGER NOT NULL, 
	pid INTEGER, 
	PRIMARY KEY (id)
);


CREATE TABLE terminal_trans_dim (
	trans_code VARCHAR(6) NOT NULL, 
	trans_name VARCHAR(50) NOT NULL, 
	PRIMARY KEY (trans_code)
);


CREATE TABLE terminal_retcode_dim (
	result_code VARCHAR(2) NOT NULL, 
	result_message VARCHAR(100) NOT NULL, 
	PRIMARY KEY (result_code)
);


CREATE TABLE shop_info (
	shop_no VARCHAR(15) NOT NULL, 
	address VARCHAR(200) DEFAULT '' NOT NULL, 
	points_rule INTEGER DEFAULT '0' NOT NULL, 
	remark TEXT DEFAULT '' NOT NULL, 
	shop_name VARCHAR(100) NOT NULL, 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	unit_no VARCHAR(4) NOT NULL, 
	PRIMARY KEY (shop_no), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE card_batch_info (
	id UUID NOT NULL default uuid_generate_v4(), 
	batch_no INTEGER NOT NULL, 
	file_generated BOOLEAN NOT NULL, 
	remark TEXT DEFAULT '' NOT NULL, 
	unit_no VARCHAR(4) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE gift (
	id UUID NOT NULL, 
	gift_name VARCHAR(255) NOT NULL, 
	points INTEGER DEFAULT '0' NOT NULL, 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	unit_no VARCHAR(4) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE role_info (
	role_no UUID NOT NULL, 
	role_name VARCHAR(100) NOT NULL, 
	create_datetime TIMESTAMP WITHOUT TIME ZONE DEFAULT 'now()' NOT NULL, 
	creator VARCHAR(20) NOT NULL, 
	remark TEXT DEFAULT '' NOT NULL, 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	unit_no VARCHAR(4) NOT NULL, 
	PRIMARY KEY (role_no), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE card_resource (
	unit_no VARCHAR(4) NOT NULL, 
	start_batch_no INTEGER NOT NULL, 
	start_card_no INTEGER NOT NULL, 
	PRIMARY KEY (unit_no), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE tmp_card_info (
	card_no VARCHAR(19) NOT NULL, 
	amount INTEGER NOT NULL, 
	times INTEGER NOT NULL DEFAULT 0,
	batch_no INTEGER NOT NULL, 
	card_kind VARCHAR(1) DEFAULT '0', 
	exp_date VARCHAR(8) DEFAULT '', 
	password VARCHAR(255) NOT NULL, 
	points INTEGER DEFAULT '0' NOT NULL, 
	points_rule FLOAT DEFAULT '0.00' NOT NULL, 
	recharge_flag BOOLEAN NOT NULL, 
	pre_status VARCHAR(1) DEFAULT '' NOT NULL,
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	track_2 VARCHAR(37) NOT NULL, 
	unit_no VARCHAR(4) NOT NULL, 
	valid_life INTEGER DEFAULT '6' NOT NULL, 
	func_deposit BOOLEAN NOT NULL DEFAULT 't',
	func_times BOOLEAN NOT NULL DEFAULT 'f',
	PRIMARY KEY (card_no), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE inter_info (
	id UUID NOT NULL, 
	credit_unit VARCHAR(4) NOT NULL, 
	debit_unit VARCHAR(4) NOT NULL, 
	remark TEXT DEFAULT '' NOT NULL, 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(credit_unit) REFERENCES unit_info (unit_no), 
	FOREIGN KEY(debit_unit) REFERENCES unit_info (unit_no)
);


CREATE TABLE member (
	id UUID NOT NULL, 
	address VARCHAR(200) DEFAULT '' NOT NULL, 
	birthday VARCHAR(8) DEFAULT '' NOT NULL, 
	province INTEGER, 
	city INTEGER, 
	country INTEGER, 
	district INTEGER, 
	email VARCHAR(255) DEFAULT '' NOT NULL, 
	idcard VARCHAR(18) DEFAULT '' NOT NULL, 
	member_name VARCHAR(20) NOT NULL, 
	name_initials VARCHAR(10) NOT NULL DEFAULT '', 
	name_pinyin VARCHAR(100) NOT NULL DEFAULT '', 
	phone VARCHAR(11) DEFAULT '' NOT NULL DEFAULT '', 
	register_datetime TIMESTAMP WITHOUT TIME ZONE DEFAULT 'now()' NOT NULL, 
	sex VARCHAR(1) DEFAULT 'F' NOT NULL, 
	shop_no VARCHAR(15) NOT NULL, 
	unit_no VARCHAR(4) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(province) REFERENCES sys_city_dim (id), 
	FOREIGN KEY(city) REFERENCES sys_city_dim (id), 
	FOREIGN KEY(country) REFERENCES sys_city_dim (id), 
	FOREIGN KEY(district) REFERENCES sys_city_dim (id), 
	FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE user_info (
	user_no VARCHAR(20) NOT NULL, 
	address VARCHAR(200) DEFAULT '' NOT NULL, 
	is_admin BOOLEAN DEFAULT 'f' NOT NULL, 
	password VARCHAR(32) DEFAULT '670b14728ad9902aecba32e22fa4f6bd' NOT NULL, 
	real_name VARCHAR(10) DEFAULT '' NOT NULL, 
	role_no UUID, 
	shop_no VARCHAR(15), 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	unit_no VARCHAR(4), 
	user_level VARCHAR(10) DEFAULT 'shop' NOT NULL, 
	PRIMARY KEY (user_no), 
	FOREIGN KEY(role_no) REFERENCES role_info (role_no), 
	FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE role_operation (
	id UUID NOT NULL default uuid_generate_v4(), 
	operation_code VARCHAR(6) NOT NULL, 
	role_no UUID NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(operation_code) REFERENCES sys_operation_dim (operation_code), 
	FOREIGN KEY(role_no) REFERENCES role_info (role_no)
);


CREATE TABLE card_group (
	id UUID NOT NULL, 	
	create_datetime TIMESTAMP WITHOUT TIME ZONE DEFAULT 'now()' NOT NULL, 
	creator VARCHAR(20) NOT NULL, 
	group_name VARCHAR(255) NOT NULL, 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	unit_no VARCHAR(4) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(creator) REFERENCES user_info (user_no), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE unit_manager (
	id UUID NOT NULL, 
	remark TEXT DEFAULT '' NOT NULL, 
	
	unit_no VARCHAR(4) NOT NULL, 
	user_no VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no), 
	FOREIGN KEY(user_no) REFERENCES user_info (user_no)
);


CREATE TABLE terminal_info (
	terminal_no VARCHAR(8) NOT NULL, 
	batch_no INTEGER DEFAULT '1' NOT NULL, 
	current_operator VARCHAR(20) NOT NULL, 
	des_key VARCHAR(36) NOT NULL, 
	is_default BOOLEAN DEFAULT 'f' NOT NULL, 
	remark TEXT DEFAULT '' NOT NULL, 
	shop_no VARCHAR(15) NOT NULL, 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	trace_no INTEGER DEFAULT '1' NOT NULL, 
	PRIMARY KEY (terminal_no), 
	FOREIGN KEY(current_operator) REFERENCES user_info (user_no), 
	FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no)
);


CREATE TABLE points_rule (
	id UUID NOT NULL, 
	create_time TIMESTAMP WITHOUT TIME ZONE DEFAULT 'now()' NOT NULL, 
	creator VARCHAR(20) NOT NULL, 
	credit_unit VARCHAR(4) NOT NULL, 
	debit_unit VARCHAR(4) NOT NULL, 
	points_rule INTEGER DEFAULT '0' NOT NULL, 
	statue VARCHAR(1) DEFAULT '0' NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(creator) REFERENCES user_info (user_no), 
	FOREIGN KEY(credit_unit) REFERENCES unit_info (unit_no), 
	FOREIGN KEY(debit_unit) REFERENCES unit_info (unit_no)
);


CREATE TABLE terminal_trans (
	id UUID NOT NULL, 
	terminal_no VARCHAR(8) NOT NULL, 
	trans_code VARCHAR(6) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(terminal_no) REFERENCES terminal_info (terminal_no), 
	FOREIGN KEY(trans_code) REFERENCES terminal_trans_dim (trans_code)
);

-- 卡状态：0新卡未启用 1正常卡 2挂失卡 3 冻结卡 4作废卡
CREATE TABLE card_info (
	card_no VARCHAR(19) NOT NULL, 
	amount INTEGER NOT NULL,
	times INTEGER NOT NULL DEFAULT 0,  -- 还有几次 
	card_kind VARCHAR(1) DEFAULT '0' NOT NULL, 
	card_group UUID, 
	member_id TEXT DEFAULT '' NOT NULL, 
	exp_date VARCHAR(8) DEFAULT '' NOT NULL, 
	password VARCHAR(32) NOT NULL, 
	points INTEGER DEFAULT '0' NOT NULL, 
	points_rule FLOAT DEFAULT '0.00' NOT NULL,
	pre_status VARCHAR(1) DEFAULT '' NOT NULL, 
	status VARCHAR(1) DEFAULT '0' NOT NULL, 
	total_pay INTEGER DEFAULT '0' NOT NULL, 
	track_2 VARCHAR(37) NOT NULL, 
	unit_no VARCHAR(4) NOT NULL, 
	valid_life INTEGER NOT NULL, 
	func_deposit BOOLEAN NOT NULL DEFAULT 't',  -- 能否充值
	func_times BOOLEAN NOT NULL DEFAULT 'f',  -- 是否是次卡
	PRIMARY KEY (card_no), 
	FOREIGN KEY(card_group) REFERENCES card_group (id), 
	FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE trans (
	id UUID NOT NULL, 
	amount INTEGER NOT NULL, 
	amount_balance INTEGER NOT NULL, 
	award_amount INTEGER DEFAULT '0' NOT NULL, 
	award_points INTEGER DEFAULT '0' NOT NULL, 
	batch_no INTEGER NOT NULL, 
	card_no VARCHAR(19) NOT NULL, 
	credit_unit VARCHAR(4) NOT NULL, 
	reversible VARCHAR(1) DEFAULT '0' NOT NULL, 
	debit_unit VARCHAR(4) NOT NULL, 
	interface VARCHAR(1) DEFAULT '0' NOT NULL, 
	points INTEGER DEFAULT '0' NOT NULL, 
	points_balance INTEGER NOT NULL, 
	points_rule FLOAT DEFAULT '0.00' NOT NULL, 
	pos_operator VARCHAR(20) NOT NULL, 
	result_code VARCHAR(2) NOT NULL, 
	shop_no VARCHAR(15) NOT NULL, 
	terminal_no VARCHAR(8) NOT NULL, 
	trace_no INTEGER NOT NULL, 
	trans_code VARCHAR(6) NOT NULL, 
	trans_date VARCHAR(8) NOT NULL, 
	trans_time VARCHAR(6) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(card_no) REFERENCES card_info (card_no), 
	FOREIGN KEY(credit_unit) REFERENCES unit_info (unit_no), 
	FOREIGN KEY(debit_unit) REFERENCES unit_info (unit_no), 
	FOREIGN KEY(pos_operator) REFERENCES user_info (user_no), 
	FOREIGN KEY(result_code) REFERENCES terminal_retcode_dim (result_code), 
	FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no), 
	FOREIGN KEY(terminal_no) REFERENCES terminal_info (terminal_no), 
	FOREIGN KEY(trans_code) REFERENCES terminal_trans_dim (trans_code)
);

 
CREATE TABLE history_trans (
	id UUID NOT NULL, 
	amount INTEGER NOT NULL, 
	amount_balance INTEGER NOT NULL, 
	award_amount INTEGER DEFAULT '0' NOT NULL, 
	award_points INTEGER DEFAULT '0' NOT NULL, 
	batch_no INTEGER NOT NULL, 
	card_no VARCHAR(19) NOT NULL, 
	credit_unit VARCHAR(4) NOT NULL, 
	reversiable VARCHAR(1) DEFAULT '0' NOT NULL, 
	debit_unit VARCHAR(4) NOT NULL, 
	interface VARCHAR(1) DEFAULT '0' NOT NULL, 
	points INTEGER DEFAULT '0' NOT NULL, 
	points_balance INTEGER NOT NULL, 
	points_rule FLOAT DEFAULT '0.00' NOT NULL, 
	pos_operator VARCHAR(20) NOT NULL, 
	result_code VARCHAR(2) NOT NULL, 
	shop_no VARCHAR(15) NOT NULL, 
	terminal_no VARCHAR(8) NOT NULL, 
	trace_no INTEGER NOT NULL, 
	trans_code VARCHAR(6) NOT NULL, 
	trans_date VARCHAR(8) NOT NULL, 
	trans_time VARCHAR(6) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(card_no) REFERENCES card_info (card_no), 
	FOREIGN KEY(credit_unit) REFERENCES unit_info (unit_no), 
	FOREIGN KEY(debit_unit) REFERENCES unit_info (unit_no), 
	FOREIGN KEY(pos_operator) REFERENCES user_info (user_no), 
	FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no), 
	FOREIGN KEY(terminal_no) REFERENCES terminal_info (terminal_no), 
	FOREIGN KEY(trans_code) REFERENCES terminal_trans_dim (trans_code)
);



-- CREATE TABLE supplier
-- (
--   id uuid default uuid_generate_v4() NOT NULL,
--   supplier_name character varying(100),
--   tel character varying(12) DEFAULT '' NOT NULL,
--   email character varying(50) DEFAULT '' NOT NULL,
--   unit_no character varying(4) NOT NULL,
--   address character varying(100) NOT NULL DEFAULT '',
--   status character varying(1) NOT NULL DEFAULT '0',
--   PRIMARY KEY(id),
--   FOREIGN KEY (unit_no) REFERENCES unit_info(unit_no)
-- );

CREATE TABLE goods_info
(
  id uuid NOT NULL,
  unit_no character varying(4) NOT NULL,
  goods_name character varying(50) NOT NULL,
  price integer NOT NULL,
  pack_unit character varying(10) NOT NULL,
  creator character varying(20) NOT NULL,
  create_time timestamp(6) without time zone,
  status character varying(1) NOT NULL DEFAULT '0',
  pinyin character varying(300) NOT NULL DEFAULT '',
  pinyin_initial character(100) NOT NULL DEFAULT '',
  barcode character varying(13) NOT NULL DEFAULT '',
  brief_code character varying(10) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  FOREIGN KEY (unit_no) REFERENCES unit_info(unit_no),
  FOREIGN KEY (creator) REFERENCES user_info(user_no)
);