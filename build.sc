import mill._, scalalib._, publish._
import mill.scalalib._
import mill.scalalib.scalafmt.ScalafmtModule
import scala.util._
import mill.bsp._

object Setting{
	def scalacOptions = Seq(
		"-Xsource:2.11",
		"-language:reflectiveCalls",
		"-deprecation",
		"-feature",
		"-Xcheckinit",
		"-P:chiselplugin:useBundlePlugin"
	)
	def scalacPluginIvyDeps = Agg(
		ivy"edu.berkeley.cs:::chisel3-plugin:3.4.4",
		ivy"org.scalamacros:::paradise:2.1.1"
	)
	def pomSettings = PomSettings(
		description = "Hello",
		organization = "io.github.carlzhang4",
		url = "https://maven.pkg.github.com/carlzhang4/chisel_common",
		licenses = Seq(License.MIT),
		versionControl = VersionControl.github("carlzhang4", "chisel_common"),
		developers = Seq(
			Developer("carlzhang4", "CJ", "https://github.com/carlzhang4")
		)
	)
}
object common extends ScalaModule  with PublishModule{
	override def scalaVersion = "2.12.13"
	override def scalacOptions = Setting.scalacOptions
	override def scalacPluginIvyDeps = Setting.scalacPluginIvyDeps
	override def ivyDeps = Agg(
		ivy"edu.berkeley.cs::chisel3:3.4.4",
	)
  
	def mainClass = Some("common.elaborate")
	def publishVersion = "0.0.1"
	def pomSettings = Setting.pomSettings
}

object qdma extends ScalaModule  with PublishModule{
	override def scalaVersion = "2.12.13"
	override def scalacOptions = Setting.scalacOptions
	override def scalacPluginIvyDeps = Setting.scalacPluginIvyDeps
	override def ivyDeps = Agg(
		ivy"edu.berkeley.cs::chisel3:3.4.4",
		ivy"io.github.carlzhang4::common:0.0.1",
	)
	def mainClass = Some("qdma.elaborate")
	def publishVersion = "0.0.1"
	def pomSettings = Setting.pomSettings
}

object smart_db extends ScalaModule { m =>
	override def scalaVersion = "2.12.13"
	override def scalacOptions = Setting.scalacOptions
	override def scalacPluginIvyDeps = Setting.scalacPluginIvyDeps
	override def ivyDeps = Agg(
		ivy"edu.berkeley.cs::chisel3:3.4.4",
		ivy"io.github.carlzhang4::common:0.0.1",
		ivy"io.github.carlzhang4::roce:0.0.1"
	)
	// def moduleDeps = Seq(lib1)
	// def unmanagedClasspath = T {Agg(
	// 	PathRef(os.Path("/home/amax/hhj/chisel_hhj/out/roce/jar.dest/out.jar"))
	// )}
	def mainClass = Some("smart_db.elaborate")
}