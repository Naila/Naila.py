from dataclasses import dataclass
from datetime import datetime
from utils.ctx import CustomContext


__author__ = "Sapphire"
__date__ = "01/22/2022"
__copyright__ = "Copyright 2020, Sapphire"
__credits__ = ["Sapphire", "Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.1"
__maintainer__ = "Sapphire"
__email__ = "Sapphire@hardinserver.com"
__status__ = "Production"

# TODO: Move to config
logch = 667894488341020693
reportchan = 667894451644923906
judgement = 667894473174286367
ds_server = 294505571317710849
banlist_judge = 667897608379039764


@dataclass
class Banlist:
    ctx: CustomContext


    async def report(self, messageid, user, reason, proof, reporter):
        ctx = self.ctx
        await ctx.pool.execute("INSERT INTO reports(messageid, id, reason, proof, reporter) VALUES($1, $2, $3, $4, $5)", messageid, user.id, reason, proof, reporter)

    async def callreport(self, messageid):
        ctx = self.ctx
        data = await ctx.pool.fetch("SELECT * FROM reports WHERE messageid=$1", messageid)
        return data

    async def approve(self, user, reason, proof, reporter):
        ctx = self.ctx
        date = datetime.now().strftime(ctx.bot.config()['time_format'])
        await ctx.pool.execute("INSERT INTO bans(id, reason, proof, reporter, date) VALUES($1, $2, $3, $4, $5)", user.id, reason, proof, reporter, date)

    async def reject(self, messageid):
        ctx = self.ctx
        await ctx.pool.execute("DELETE FROM reports where messageid=$1", messageid)

    async def lookup(self, user):
        ctx = self.ctx
        data = await ctx.pool.fetch("SELECT * FROM bans WHERE id=$1", user.id)
        return data

    async def revoke(self, user):
        ctx = self.ctx
        await ctx.pool.execute("DELETE FROM reports where id=$1", user)

    async def appeal(self, user):
        ctx = self.ctx
        date = datetime.now().strftime(ctx.bot.config()['time_format'])
        await ctx.pool.execute("INSERT INTO appeals(id, reason, proof, date) VALUES($1, $2, $3, $4)", user.id, reason, proof, date)
