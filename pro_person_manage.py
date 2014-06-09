#Role,Employee,Client
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import os.path
import torndb
import tornado.autoreload
import hashlib
import json
import tornado.escape
from tornado.options import define, options


define("port", default=8888, help="run on the given port", type=int)
define("mysql_host",default="localhost", help="the pro_mange database host")
define("mysql_user",default="root", help="the pro_mange database user")
define("mysql_pass",default="root", help="the pro_mange database password")
define("mysql_database",default="pro", help="the pro_mange database ")

class Application(tornado.web.Application):
	def __init__(self):
		handles = [
			(r'/',LoginHandler),
			(r'/add_role',AddRoleHandler),
			(r'/add_employee',AddEmployeeHandler),
			(r'/add_client',AddClientHandler),
			(r'/list_role',ListRoleHandler),
			(r'/list_employee',ListEmployeeHandler),
			(r'/list_client',ListClientHandler),
			(r'/del_num',DelHandler),
			(r'/get_all',GetAllHandler),
			(r'/my_pro',MyPro),
			
		]
		cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
		settings = dict(
				template_path = os.path.join(os.path.dirname(__file__),"template"),
				static_path = os.path.join(os.path.dirname(__file__),"static"),
				cookie_secret = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",

			)
		tornado.web.Application.__init__(self,handles,**settings)

		self.db = torndb.Connection(
			host=options.mysql_host,database=options.mysql_database,
			user=options.mysql_user,password=options.mysql_pass
			)

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db
	def get_current_user(self):
		user_name = self.get_secure_cookie("user")
		if not user_name: return None
		return 	user_name
	def get_user_power(self):
		names = self.get_current_user()
		power = self.db.get("SELECT power FROM Employee right join Role on Employee.roleNo=Role.roleNo WHERE Employee.Name= %s",names);
		if not power: return None
		return power
	def get_encodepass(self,user_pass):
		m=hashlib.md5()
		m.update(user_pass)
		return m.hexdigest()
		
class LoginHandler(BaseHandler):
	def get(self):	
		self.render("per_login.html")
	def post(self):
		name = self.get_argument("login_user")
		password = self.get_argument("login_pass")
		m=hashlib.md5()
		m.update(password)
		password_code = m.hexdigest()
		isname = None
		if name:
			isname = self.db.get("SELECT pass FROM Employee WHERE Name = %s",name)
			if isname['pass']==password_code:
				self.set_secure_cookie("user",name)
				self.redirect("/list_employee")

			else:

				self.redirect("/")


class AddRoleHandler(BaseHandler):
		"""add role process"""
		def get(self):
			if self.get_current_user():
				entries = self.db.query("SELECT role_name,power FROM Role WHERE power!=9 AND power!=3 ")

				self.render("per_add_role.html",entries=entries)
			else:
				redirect("/")

		def post(self):
			
			role_name = self.get_argument("role_name")
			role_textarea = self.get_argument("role_textarea")
			role_power = self.get_argument("role_power")
			self.db.execute("INSERT INTO Role (role_name,description,power,create_time)"
				"VALUES (%s,%s,%s,UTC_TIMESTAMP())",role_name,role_textarea,role_power)


class AddEmployeeHandler(BaseHandler):
		def get(self):
			if self.get_current_user():
				entries = self.db.query("SELECT role_name,roleNo FROM Role WHERE power!=9 AND power!=3 ")

				self.render("per_add_employee.html",entries=entries)

			else:
				redirect("/")
		def post(self):
			emp_name = self.get_argument("emp_name")
			emp_pass = self.get_argument("emp_pass")
			emp_tel = self.get_argument("emp_tel")
			emp_addr = self.get_argument("emp_addr")
			emp_email = self.get_argument("emp_email")
			emp_sex = self.get_argument("emp_sex")
			emp_power = self.get_argument("emp_power")
			newemp_pass = self.get_encodepass(emp_pass)
			self.db.execute("INSERT INTO Employee (Name,address,pass,telNo,empEmailAddress,sex,roleNo,datestartRole,salary,EmployeeState)"
				"VALUES(%s,%s,%s,%s,%s,%s,%s,UTC_TIMESTAMP(),1000,0)",emp_name,emp_addr,newemp_pass,emp_tel,emp_email,emp_sex,emp_power)
			

class AddClientHandler(BaseHandler):
		def get(self):
			if self.get_current_user():	
				self.render("per_add_client.html")
			else:
				redirect("/")
		def post(self):
			cli_name = self.get_argument("cli_name")
			cli_pass = self.get_argument("cli_pass")
			cli_tel = self.get_argument("cli_tel")
			cli_qq = self.get_argument("cli_qq")
			cli_email = self.get_argument("cli_email")
			role_sex = self.get_argument("role_sex")
			newcli_pass = self.get_encodepass(cli_pass) 
			self.db.execute("INSERT INTO Client (clientName,clientPss,clientTelNo,qq,contactEmailAddress,sex,role_No,clientState)"
							"VALUES(%s,%s,%s,%s,%s,%s,1104,0)",cli_name,newcli_pass,cli_tel,cli_qq,cli_email,role_sex)
	

class ListRoleHandler(BaseHandler):
		def get(self):
			if self.get_current_user():
				entries = self.db.query("SELECT * FROM Role")
				self.render("per_list_role.html",entries=entries)
			else:
				redirect("/")


class ListEmployeeHandler(BaseHandler):
		def get(self):
			if self.get_current_user():
				entries = self.db.query("SELECT * FROM Employee,Role WHERE Employee.roleNo=Role.roleNo")
				self.render("per_list_employee.html",entries=entries)
			else:
				redirect("/")


class ListClientHandler(BaseHandler):
	def get(self):
		if self.get_current_user:
			entries = self.db.query("SELECT * FROM Client")
			self.render("per_list_client.html",entries=entries)
		else:
			redirect("/")

class DelHandler(BaseHandler):
	def post(self):
		num_id = self.get_argument("num_id",None)
		name = self.get_argument("num_name",None)
		if name=="role":
			self.db.execute("DELETE FROM Role WHERE roleNo=%s",num_id)
		if name=="emp":
			self.db.execute("DELETE FROM Employee WHERE EmployeeNo=%s",num_id)
		if name=="cli":
			self.db.execute("DELETE FROM Client WHERE clientNO=%s",num_id)		


class GetAllHandler(BaseHandler):
	 
	def post(self):
		self.set_header('Content-Type', 'text/javascript')
		num_id = self.get_argument("num_id",None)
		name = self.get_argument("num_name",None)
		if name=="emp":
			entry=self.db.get("SELECT * FROM Employee,Role WHERE EmployeeNo=%s AND Employee.roleNo=Role.roleNo",num_id)
			dict={'EmployeeNo':entry.EmployeeNo,
					'Name':entry.Name,
					'address':entry.address,
					'telNo':entry.telNo,
					'empEmailAddress':entry.empEmailAddress,
					'sex':entry.sex,
					'salary':entry.salary,
					'roleNo':entry.roleNo,
					'role_name':entry.role_name,
					
					}
		
			self.write(dict)

		if name=="cli":
			entry=self.db.get("SELECT * FROM Client WHERE clientNo=%s",num_id)
			dict={
				'clientNo':entry.clientNo,
				'clientName':entry.clientName,
				'clientTelNo':entry.clientTelNo,
				'qq':entry.qq,
				'contactEmailAddress':entry.contactEmailAddress,
				'sex':entry.sex,

			}
			self.write(dict)
		if name=="role":
			entry=self.db.get("SELECT * FROM Role WHERE roleNo=%s",num_id)
			dict={
				'role_name':entry.role_name,
				'description':entry.description,
				'power':entry.power,
			}
			self.write(dict)

# class UpdateHandler(BaseHandler):  #update all 
# 	def post(self):

class MyPro(BaseHandler):
	def get(self):
		self.render("my_pro.html")

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	loop=tornado.ioloop.IOLoop.instance()
	tornado.autoreload.start(loop)
	loop.start()
if __name__ == "__main__":
	main()
