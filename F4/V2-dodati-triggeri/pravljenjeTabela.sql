
CREATE TABLE [connections]
( 
	[follower_id]        int  NOT NULL ,
	[followee_id]        int  NOT NULL ,
	[follow_date]        timestamp  NULL ,
	[status]             nvarchar(255)  NULL 
)
go

CREATE TABLE [event_reviews]
( 
	[event_id]           int  NOT NULL ,
	[user_id]            int  NOT NULL ,
	[comment]            text  NULL ,
	[created_at]         timestamp  NULL ,
	[count_id]           int  NOT NULL 
)
go

CREATE TABLE [event_user]
( 
	[event_id]           int  NOT NULL ,
	[user_id]            int  NOT NULL ,
	[status]             nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_239_1316130210]
		CHECK  ( [status]='interested' OR [status]='going' OR [status]='attended' ),
	[created_at]         timestamp  NULL ,
	[rating]             int  NULL 
)
go

CREATE TABLE [events]
( 
	[event_id]           int  IDENTITY  NOT NULL ,
	[name]               nvarchar(255)  NULL ,
	[description]        text  NULL ,
	[date]               date  NULL ,
	[time]               time  NULL ,
	[org_id]             int  NULL ,
	[status]             nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_199_619956948]
		CHECK  ( [status]='draft' OR [status]='published' OR [status]='cancelled' ),
	[type]               nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_201_743721440]
		CHECK  ( [type]='party' OR [type]='sport_tournament' ),
	[picture]            nvarchar(255)  NULL ,
	[total_rating]       int  NULL ,
	[count_rating]       int  NULL ,
	[created_at]         timestamp  NULL ,
	[place_id]           int  NULL 
)
go

CREATE TABLE [faculties]
( 
	[faculty_id]         int  IDENTITY  NOT NULL ,
	[name]               nvarchar(255)  NULL ,
	[city]               nvarchar(255)  NULL ,
	[tag]                nvarchar(255)  NULL 
)
go

CREATE TABLE [notifications]
( 
	[notification_id]    int  IDENTITY  NOT NULL ,
	[user_id]            int  NULL ,
	[from_id]            int  NULL ,
	[from_type]          nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_278_234883209]
		CHECK  ( [from_type]='user' OR [from_type]='organization' ),
	[message]            text  NULL ,
	[type]               nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_281_1500998016]
		CHECK  ( [type]='connection_request' OR [type]='event_invite' OR [type]='event_reminder' OR [type]='standard' ),
	[status]             nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_283_1284700413]
		CHECK  ( [status]='unread' OR [status]='read' ),
	[created_at]         timestamp  NULL 
)
go

CREATE TABLE [organization_user]
( 
	[org_id]             int  NOT NULL ,
	[user_id]            int  NOT NULL ,
	[role]               nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_249_234816994]
		CHECK  ( [role]='member' OR [role]='admin' ),
	[join_date]          date  NULL 
)
go

CREATE TABLE [organizations]
( 
	[org_id]             int  IDENTITY  NOT NULL ,
	[name]               nvarchar(255)  NULL ,
	[description]        text  NULL ,
	[picture]            nvarchar(255)  NULL ,
	[total_rating]       int  NULL ,
	[count_rating]       int  NULL ,
	[created_at]         timestamp  NULL 
)
go

CREATE TABLE [places]
( 
	[place_id]           int  IDENTITY  NOT NULL ,
	[name]               nvarchar(255)  NULL ,
	[description]        nvarchar(255)  NULL ,
	[working_hours]      nvarchar(255)  NULL ,
	[address]            nvarchar(255)  NULL ,
	[type]               nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_228_911758045]
		CHECK  ( [type]='bar' OR [type]='klub' OR [type]='kafana' OR [type]='splav' OR [type]='kafic' ),
	[picture]            nvarchar(255)  NULL ,
	[total_rating]       int  NULL ,
	[count_rating]       int  NULL ,
	[google_maps_url]    nvarchar(255)  NULL 
)
go

CREATE TABLE [student_org]
( 
	[org_id]             int  NOT NULL ,
	[faculty_id]         int  NOT NULL 
)
go

CREATE TABLE [users]
( 
	[user_id]            int  IDENTITY  NOT NULL ,
	[username]           nvarchar(255)  NULL ,
	[email]              nvarchar(255)  NULL ,
	[password]           nvarchar(255)  NULL ,
	[full_name]          nvarchar(255)  NULL ,
	[date_birth]         date  NULL ,
	[gender]             nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_177_1045290468]
		CHECK  ( [gender]='M' OR [gender]='F' ),
	[city]               nvarchar(255)  NULL ,
	[faculty_id]         int  NOT NULL ,
	[instagram_link]     nvarchar(255)  NULL ,
	[profile_picture]    nvarchar(255)  NULL ,
	[bio]                text  NULL ,
	[role]               nvarchar(255)  NOT NULL 
	CONSTRAINT [Validation_Rule_184_759780680]
		CHECK  ( [role]='regular' OR [role]='organizer' OR [role]='admin' ),
	[unread_notifications] int  NULL ,
	[created_at]         timestamp  NULL 
)
go

ALTER TABLE [connections]
	ADD CONSTRAINT [XPKconnections] PRIMARY KEY  NONCLUSTERED ([follower_id] ASC,[followee_id] ASC)
go

ALTER TABLE [event_reviews]
	ADD CONSTRAINT [XPKevent_reviews] PRIMARY KEY  NONCLUSTERED ([event_id] ASC,[user_id] ASC,[count_id] ASC)
go

ALTER TABLE [event_user]
	ADD CONSTRAINT [XPKevent_user] PRIMARY KEY  NONCLUSTERED ([event_id] ASC,[user_id] ASC)
go

ALTER TABLE [events]
	ADD CONSTRAINT [XPKevents] PRIMARY KEY  NONCLUSTERED ([event_id] ASC)
go

ALTER TABLE [faculties]
	ADD CONSTRAINT [XPKfaculties] PRIMARY KEY  NONCLUSTERED ([faculty_id] ASC)
go

ALTER TABLE [faculties]
	ADD CONSTRAINT [faculties.name] UNIQUE ([name]  ASC)
go

ALTER TABLE [notifications]
	ADD CONSTRAINT [XPKnotifications] PRIMARY KEY  NONCLUSTERED ([notification_id] ASC)
go

ALTER TABLE [organization_user]
	ADD CONSTRAINT [XPKorganization_user] PRIMARY KEY  NONCLUSTERED ([org_id] ASC,[user_id] ASC)
go

ALTER TABLE [organizations]
	ADD CONSTRAINT [XPKorganizations] PRIMARY KEY  NONCLUSTERED ([org_id] ASC)
go

ALTER TABLE [organizations]
	ADD CONSTRAINT [organization.name] UNIQUE ([name]  ASC)
go

ALTER TABLE [places]
	ADD CONSTRAINT [XPKplaces] PRIMARY KEY  NONCLUSTERED ([place_id] ASC)
go

ALTER TABLE [student_org]
	ADD CONSTRAINT [XPKstudent_org] PRIMARY KEY  CLUSTERED ([org_id] ASC)
go

ALTER TABLE [users]
	ADD CONSTRAINT [XPKusers] PRIMARY KEY  NONCLUSTERED ([user_id] ASC)
go

ALTER TABLE [users]
	ADD CONSTRAINT [user.name] UNIQUE ([username]  ASC)
go

ALTER TABLE [users]
	ADD CONSTRAINT [user.email] UNIQUE ([email]  ASC)
go


ALTER TABLE [connections]
	ADD CONSTRAINT [R_7] FOREIGN KEY ([follower_id]) REFERENCES [users]([user_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go

ALTER TABLE [connections]
	ADD CONSTRAINT [R_8] FOREIGN KEY ([followee_id]) REFERENCES [users]([user_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go


ALTER TABLE [event_reviews]
	ADD CONSTRAINT [R_12] FOREIGN KEY ([event_id]) REFERENCES [events]([event_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go

ALTER TABLE [event_reviews]
	ADD CONSTRAINT [R_13] FOREIGN KEY ([user_id]) REFERENCES [users]([user_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go


ALTER TABLE [event_user]
	ADD CONSTRAINT [R_3] FOREIGN KEY ([event_id]) REFERENCES [events]([event_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go

ALTER TABLE [event_user]
	ADD CONSTRAINT [R_4] FOREIGN KEY ([user_id]) REFERENCES [users]([user_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go


ALTER TABLE [events]
	ADD CONSTRAINT [R_1] FOREIGN KEY ([place_id]) REFERENCES [places]([place_id])
		ON UPDATE CASCADE
go

ALTER TABLE [events]
	ADD CONSTRAINT [R_2] FOREIGN KEY ([org_id]) REFERENCES [organizations]([org_id])
		ON UPDATE CASCADE
go


ALTER TABLE [notifications]
	ADD CONSTRAINT [R_11] FOREIGN KEY ([user_id]) REFERENCES [users]([user_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go


ALTER TABLE [organization_user]
	ADD CONSTRAINT [R_5] FOREIGN KEY ([org_id]) REFERENCES [organizations]([org_id])
		ON UPDATE CASCADE
go

ALTER TABLE [organization_user]
	ADD CONSTRAINT [R_6] FOREIGN KEY ([user_id]) REFERENCES [users]([user_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go


ALTER TABLE [student_org]
	ADD CONSTRAINT [R_14] FOREIGN KEY ([org_id]) REFERENCES [organizations]([org_id])
		ON DELETE CASCADE
		ON UPDATE CASCADE
go

ALTER TABLE [student_org]
	ADD CONSTRAINT [R_15] FOREIGN KEY ([faculty_id]) REFERENCES [faculties]([faculty_id])
		ON UPDATE CASCADE
go


ALTER TABLE [users]
	ADD CONSTRAINT [R_9] FOREIGN KEY ([faculty_id]) REFERENCES [faculties]([faculty_id])
		ON UPDATE CASCADE
go
